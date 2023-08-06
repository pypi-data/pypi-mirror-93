import {Injectable} from "@angular/core";

import {
    extend,
    Payload,
    PayloadEnvelope,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService,
    TupleSelector,
    TupleStorageFactoryService,
    VortexService,
    VortexStatusService
} from "@synerty/vortexjs";

import {branchIndexStorageName, diagramFilt, diagramTuplePrefix} from "../PluginNames";


import {Subject} from "rxjs/Subject";
import {Observable} from "rxjs/Observable";
import {BranchIndexEncodedChunkTuple} from "./BranchIndexEncodedChunkTuple";
import {BranchIndexUpdateDateTuple} from "./BranchIndexUpdateDateTuple";
import {BranchTuple} from "../branch/BranchTuple";
import {PrivateDiagramTupleService} from "../services/PrivateDiagramTupleService";
import {BranchIndexLoaderStatusTuple} from "./BranchIndexLoaderStatusTuple";

import {OfflineConfigTuple} from "../tuples/OfflineConfigTuple";
import {ModelSet} from "../tuples/ModelSet";
import {BranchIndexLoaderServiceA} from "./BranchIndexLoaderServiceA";

// ----------------------------------------------------------------------------

export interface BranchIndexResultI {
    [key: string]: BranchTuple[]
}

// ----------------------------------------------------------------------------

let clientBranchIndexWatchUpdateFromDeviceFilt = extend(
    {'key': "clientBranchIndexWatchUpdateFromDevice"},
    diagramFilt
);

const cacheAll = "cacheAll";

// ----------------------------------------------------------------------------
/** BranchIndexChunkTupleSelector
 *
 * This is just a short cut for the tuple selector
 */

class BranchIndexChunkTupleSelector extends TupleSelector {

    constructor(private chunkKey: string) {
        super(diagramTuplePrefix + "BranchIndexChunkTuple", {key: chunkKey});
    }

    toOrderedJsonStr(): string {
        return this.chunkKey;
    }
}

// ----------------------------------------------------------------------------
/** UpdateDateTupleSelector
 *
 * This is just a short cut for the tuple selector
 */
class UpdateDateTupleSelector extends TupleSelector {
    constructor() {
        super(BranchIndexUpdateDateTuple.tupleName, {});
    }
}


// ----------------------------------------------------------------------------
/** hash method
 */
let BUCKET_COUNT = 8192;

function keyChunk(modelSetKey: string, key: string): string {
    /** Object ID Chunk

     This method creates an int from 0 to MAX, representing the hash bucket for this
     object Id.

     This is simple, and provides a reasonable distribution

     @param modelSetKey: The key of the model set that the branchIndexs are in
     @param key: The key of the branchIndex to get the chunk key for

     @return: The bucket / chunkKey where you'll find the object with this ID

     */
    if (key == null || key.length == 0)
        throw new Error("key is None or zero length");

    let bucket = 0;

    for (let i = 0; i < key.length; i++) {
        bucket = ((bucket << 5) - bucket) + key.charCodeAt(i);
        bucket |= 0; // Convert to 32bit integer
    }

    bucket = bucket & (BUCKET_COUNT - 1);

    return `${modelSetKey}.${bucket}`;
}


// ----------------------------------------------------------------------------
/** BranchIndex Cache
 *
 * This class has the following responsibilities:
 *
 * 1) Maintain a local storage of the index
 *
 * 2) Return DispKey index-blueprint based on the index.
 *
 */
@Injectable()
export class BranchIndexLoaderService extends BranchIndexLoaderServiceA {

    private UPDATE_CHUNK_FETCH_SIZE = 5;
    private OFFLINE_CHECK_PERIOD_MS = 15 * 60 * 1000; // 15 minutes

    private index = new BranchIndexUpdateDateTuple();
    private askServerChunks: BranchIndexUpdateDateTuple[] = [];

    private _hasLoaded = false;

    private _hasLoadedSubject: Subject<boolean> = new Subject<boolean>();
    private storage: TupleOfflineStorageService;

    private _statusSubject = new Subject<BranchIndexLoaderStatusTuple>();
    private _status = new BranchIndexLoaderStatusTuple();

    private modelSetByIds: { [id: number]: ModelSet } = {};
    private _hasModelSetLoaded = false;

    private offlineConfig: OfflineConfigTuple = new OfflineConfigTuple();


    constructor(private vortexService: VortexService,
                private vortexStatusService: VortexStatusService,
                storageFactory: TupleStorageFactoryService,
                private tupleService: PrivateDiagramTupleService) {
        super();

        this.tupleService.offlineObserver
            .subscribeToTupleSelector(new TupleSelector(OfflineConfigTuple.tupleName, {}),
                false, false, true)
            .takeUntil(this.onDestroyEvent)
            .filter(v => v.length != 0)
            .subscribe((tuples: OfflineConfigTuple[]) => {
                this.offlineConfig = tuples[0];
                if (this.offlineConfig.cacheChunksForOffline)
                    this.initialLoad();
                this._notifyStatus();
            });

        let modelSetTs = new TupleSelector(ModelSet.tupleName, {});
        this.tupleService.offlineObserver
            .subscribeToTupleSelector(modelSetTs)
            .takeUntil(this.onDestroyEvent)
            .subscribe((tuples: ModelSet[]) => {
                this.modelSetByIds = {};
                for (let item of tuples) {
                    this.modelSetByIds[item.id] = item;
                }
                this._hasModelSetLoaded = true;
                this._notifyReady();
            });

        this.storage = new TupleOfflineStorageService(
            storageFactory,
            new TupleOfflineStorageNameService(branchIndexStorageName)
        );

        this.setupVortexSubscriptions();
        this._notifyStatus();

        // Check for updates every so often
        Observable.interval(this.OFFLINE_CHECK_PERIOD_MS)
            .takeUntil(this.onDestroyEvent)
            .subscribe(() => this.askServerForUpdates());
    }

    isReady(): boolean {
        return this._hasLoaded;
    }

    isReadyObservable(): Observable<boolean> {
        return this._hasLoadedSubject;
    }


    statusObservable(): Observable<BranchIndexLoaderStatusTuple> {
        return this._statusSubject;
    }

    status(): BranchIndexLoaderStatusTuple {
        return this._status;
    }

    private _notifyReady(): void {
        if (this._hasModelSetLoaded && this._hasLoaded)
            this._hasLoadedSubject.next();
    }

    private _notifyStatus(): void {
        this._status.cacheForOfflineEnabled = this.offlineConfig.cacheChunksForOffline;
        this._status.initialLoadComplete = this.index.initialLoadComplete;

        this._status.loadProgress = Object.keys(this.index.updateDateByChunkKey).length;
        for (let chunk of this.askServerChunks)
            this._status.loadProgress -= Object.keys(chunk.updateDateByChunkKey).length;

        this._statusSubject.next(this._status);
    }

    /** Initial load
     *
     * Load the dates of the index buckets and ask the server if it has any updates.
     */
    private initialLoad(): void {

        this.storage.loadTuples(new UpdateDateTupleSelector())
            .then((tuplesAny: any[]) => {
                let tuples: BranchIndexUpdateDateTuple[] = tuplesAny;
                if (tuples.length != 0) {
                    this.index = tuples[0];

                    if (this.index.initialLoadComplete) {
                        this._hasLoaded = true;
                        this._notifyReady();
                    }

                }

                this.askServerForUpdates();
                this._notifyStatus();
            });

        this._notifyStatus();
    }

    private setupVortexSubscriptions(): void {

        // Services don't have destructors, I'm not sure how to unsubscribe.
        this.vortexService.createEndpointObservable(this, clientBranchIndexWatchUpdateFromDeviceFilt)
            .takeUntil(this.onDestroyEvent)
            .subscribe((payloadEnvelope: PayloadEnvelope) => {
                this.processBranchIndexsFromServer(payloadEnvelope);
            });

        // If the vortex service comes back online, update the watch grids.
        this.vortexStatusService.isOnline
            .filter(isOnline => isOnline == true)
            .takeUntil(this.onDestroyEvent)
            .subscribe(() => this.askServerForUpdates());

    }

    private areWeTalkingToTheServer(): boolean {
        return this.offlineConfig.cacheChunksForOffline
            && this.vortexStatusService.snapshot.isOnline;
    }


    /** Ask Server For Updates
     *
     * Tell the server the state of the chunks in our index and ask if there
     * are updates.
     *
     */
    private askServerForUpdates() {
        if (!this.areWeTalkingToTheServer()) return;

        // If we're still caching, then exit
        if (this.askServerChunks.length != 0) {
            this.askServerForNextUpdateChunk();
            return;
        }

        this.tupleService.observer
            .pollForTuples(new UpdateDateTupleSelector())
            .then((tuplesAny: any) => {
                let serverIndex: BranchIndexUpdateDateTuple = tuplesAny[0];
                let keys = Object.keys(serverIndex.updateDateByChunkKey);
                let keysNeedingUpdate: string[] = [];

                this._status.loadTotal = keys.length;

                // Tuples is an array of strings
                for (let chunkKey of keys) {
                    if (!this.index.updateDateByChunkKey.hasOwnProperty(chunkKey)) {
                        this.index.updateDateByChunkKey[chunkKey] = null;
                        keysNeedingUpdate.push(chunkKey);

                    } else if (this.index.updateDateByChunkKey[chunkKey]
                        != serverIndex.updateDateByChunkKey[chunkKey]) {
                        keysNeedingUpdate.push(chunkKey);
                    }
                }
                this.queueChunksToAskServer(keysNeedingUpdate);
            });
    }


    /** Queue Chunks To Ask Server
     *
     */
    private queueChunksToAskServer(keysNeedingUpdate: string[]) {
        if (!this.areWeTalkingToTheServer()) return;

        this.askServerChunks = [];

        let count = 0;
        let indexChunk = new BranchIndexUpdateDateTuple();

        for (let key of keysNeedingUpdate) {
            indexChunk.updateDateByChunkKey[key] = this.index.updateDateByChunkKey[key];
            count++;

            if (count == this.UPDATE_CHUNK_FETCH_SIZE) {
                this.askServerChunks.push(indexChunk);
                count = 0;
                indexChunk = new BranchIndexUpdateDateTuple();
            }
        }

        if (count)
            this.askServerChunks.push(indexChunk);

        this.askServerForNextUpdateChunk();

        this._status.lastCheck = new Date();
    }

    private askServerForNextUpdateChunk() {
        if (!this.areWeTalkingToTheServer()) return;

        if (this.askServerChunks.length == 0)
            return;

        let indexChunk: BranchIndexUpdateDateTuple = this.askServerChunks.pop();
        let filt = extend({}, clientBranchIndexWatchUpdateFromDeviceFilt);
        filt[cacheAll] = true;
        let pl = new Payload(filt, [indexChunk]);
        this.vortexService.sendPayload(pl);

        this._status.lastCheck = new Date();
        this._notifyStatus();
    }


    /** Process BranchIndexes From Server
     *
     * Process the grids the server has sent us.
     */
    private processBranchIndexsFromServer(payloadEnvelope: PayloadEnvelope) {

        if (payloadEnvelope.result != null && payloadEnvelope.result != true) {
            console.log(`ERROR: ${payloadEnvelope.result}`);
            return;
        }

        payloadEnvelope
            .decodePayload()
            .then((payload: Payload) => this.storeBranchIndexPayload(payload))
            .then(() => {
                if (this.askServerChunks.length == 0) {
                    this.index.initialLoadComplete = true;
                    this._hasLoaded = true;
                    this._hasLoadedSubject.next();

                } else if (payloadEnvelope.filt[cacheAll] == true) {
                    this.askServerForNextUpdateChunk();

                }

            })
            .then(() => this._notifyStatus())
            .catch(e =>
                `BranchIndexCache.processBranchIndexsFromServer failed: ${e}`
            );

    }

    private storeBranchIndexPayload(payload: Payload) {

        let tuplesToSave: BranchIndexEncodedChunkTuple[] = <BranchIndexEncodedChunkTuple[]>payload.tuples;
        if (tuplesToSave.length == 0)
            return;

        // 2) Store the index
        this.storeBranchIndexChunkTuples(tuplesToSave)
            .then(() => {
                // 3) Store the update date

                for (let diagramIndex of tuplesToSave) {
                    this.index.updateDateByChunkKey[diagramIndex.chunkKey] = diagramIndex.lastUpdate;
                }

                return this.storage.saveTuples(
                    new UpdateDateTupleSelector(), [this.index]
                );

            })
            .catch(e => console.log(
                `BranchIndexCache.storeBranchIndexPayload: ${e}`));

    }

    /** Store Index Bucket
     * Stores the index bucket in the local db.
     */
    private storeBranchIndexChunkTuples(encodedBranchIndexChunkTuples: BranchIndexEncodedChunkTuple[]): Promise<void> {
        let retPromise: any;
        retPromise = this.storage.transaction(true)
            .then((tx) => {

                let promises = [];

                for (let encodedBranchIndexChunkTuple of encodedBranchIndexChunkTuples) {
                    promises.push(
                        tx.saveTuplesEncoded(
                            new BranchIndexChunkTupleSelector(encodedBranchIndexChunkTuple.chunkKey),
                            encodedBranchIndexChunkTuple.encodedData
                        )
                    );
                }

                return Promise.all(promises)
                    .then(() => tx.close());
            });
        return retPromise;
    }


    /** Get BranchIndexs
     *
     * Get the objects with matching keywords from the index..
     *
     * @param: modelSetKey: The model set that the branches live in
     * @param: coordSetId: Get the branch that lives in this coordSet, or null to return
     *          branches living in all coord sets.
     * @param: keys: The keys to load the branches for.
     *
     */
    getBranches(modelSetKey: string,
                coordSetId: number | null,
                keys: string[]): Promise<BranchIndexResultI> {
        if (modelSetKey == null || modelSetKey.length == 0) {
            Promise.reject("We've been passed a null/empty modelSetKey");
        }

        if (keys == null || keys.length == 0) {
            Promise.reject("We've been passed a null/empty keys");
        }

        // If there is no offline support, or we're online
        if (!this.offlineConfig.cacheChunksForOffline
            || this.vortexStatusService.snapshot.isOnline) {
            let ts = new TupleSelector(BranchTuple.tupleName, {
                "modelSetKey": modelSetKey,
                "coordSetId": coordSetId,
                "keys": keys
            });

            let isOnlinePromise: any = this.vortexStatusService.snapshot.isOnline ?
                Promise.resolve() :
                this.vortexStatusService.isOnline
                    .filter(online => online)
                    .first()
                    .toPromise();

            return isOnlinePromise
                .then(() => this.tupleService.offlineObserver.pollForTuples(ts, false))
                .then((docs: BranchTuple[]) => this._populateAndIndexObjectTypes(docs));
        }


        // If we do have offline support
        if (this.isReady())
            return this.getBranchesWhenReady(modelSetKey, coordSetId, keys)
                .then(docs => this._populateAndIndexObjectTypes(docs));

        return this.isReadyObservable()
            .first()
            .toPromise()
            .then(() => this.getBranchesWhenReady(modelSetKey, coordSetId, keys))
            .then(docs => this._populateAndIndexObjectTypes(docs));
    }


    /** Get BranchIndexs When Ready
     *
     * Get the objects with matching keywords from the index..
     *
     */
    private getBranchesWhenReady(
        modelSetKey: string, coordSetId: number, keys: string[]): Promise<BranchTuple[]> {

        let keysByChunkKey: { [key: string]: string[]; } = {};
        let chunkKeys: string[] = [];

        for (let key of keys) {
            let chunkKey: string = keyChunk(modelSetKey, key);
            if (keysByChunkKey[chunkKey] == null)
                keysByChunkKey[chunkKey] = [];
            keysByChunkKey[chunkKey].push(key);
            chunkKeys.push(chunkKey);
        }


        let promises = [];
        for (let chunkKey of chunkKeys) {
            let keysForThisChunk = keysByChunkKey[chunkKey];
            promises.push(
                this.getBranchesForKeys(coordSetId, keysForThisChunk, chunkKey)
            );
        }

        return Promise.all(promises)
            .then((promiseResults: BranchTuple[][]) => {
                let objects: BranchTuple[] = [];
                for (let results of  promiseResults) {
                    for (let result of results) {
                        objects.push(result);
                    }
                }
                return objects;
            });
    }


    /** Get BranchIndexs for Object ID
     *
     * Get the objects with matching keywords from the index..
     *
     */
    private getBranchesForKeys(coordSetId: number, keys: string[], chunkKey: string): Promise<BranchTuple[]> {

        if (!this.index.updateDateByChunkKey.hasOwnProperty(chunkKey)) {
            console.log(`ObjectIDs: ${keys} doesn't appear in the index`);
            return Promise.resolve([]);
        }

        let retPromise: any;
        retPromise = this.storage
            .loadTuplesEncoded(new BranchIndexChunkTupleSelector(chunkKey))
            .then((vortexMsg: string) => {
                if (vortexMsg == null) {
                    return [];
                }


                return Payload.fromEncodedPayload(vortexMsg)
                    .then((payload: Payload) => JSON.parse(<any>payload.tuples))
                    .then((chunkData: { [key: number]: string; }) => {

                        let foundBranchIndexs: BranchTuple[] = [];

                        for (let key of keys) {
                            // Find the keyword, we're just iterating
                            if (!chunkData.hasOwnProperty(key)) {
                                console.log(
                                    `WARNING: BranchIndex ${key} is missing from index,`
                                    + ` chunkKey ${chunkKey}`
                                );
                                continue;
                            }

                            let packedJsons = chunkData[key];
                            for (let packedJson of packedJsons) {
                                let branch = BranchTuple.unpackJson(packedJson);
                                if (branch.coordSetId == coordSetId || coordSetId == null)
                                    foundBranchIndexs.push(branch);
                            }

                        }

                        return foundBranchIndexs;

                    });
            });

        return retPromise;

    }

    private _populateAndIndexObjectTypes(results: BranchTuple[]): BranchIndexResultI {

        let objects: { [key: string]: BranchTuple[] } = {};
        for (let result of results) {
            if (objects[result.key] == null)
                objects[result.key] = [];
            objects[result.key].push(result);
        }
        return objects;
    }


}