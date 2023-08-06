import {Observable} from "rxjs/Observable";

export interface PositionUpdatedI {
    coordSetKey: string;
    x: number;
    y: number;
    zoom: number;
    editingBranch: string | null;
}

export interface OptionalPositionArgsI {
    editingBranch?: string | null;
    highlightKey?: string | null;
}

export interface DispKeyLocation {
    modelSetKey: string;
    coordSetKey: string;
    dispKey: string;
    positions: { x: number, y: number }[];
    zoom: number;
}

/** Diagram Position Service
 *
 * This service allows other plugins embedding the diagram to position the diagram.
 *
 */
export abstract class DiagramPositionService {
    constructor() {

    }

    /** Position Initial
     *
     * Loads a coordSet and positions it at the default coordinates.
     *
     * @param coordSetKey; The key of the coordSet to position on.
     */
    abstract positionByCoordSet(modelSetKey:string, coordSetKey: string): void ;

    /** Position
     *
     * @param coordSetKey: The key of the coordinate set to position.
     *                      If this doesn't match the current coord set, nothing will
     *                      happen.
     *
     * @param x: The X coordinate to position to.
     * @param y: The Y coordinate to position to.
     * @param zoom: The Zoom to set when positioning the diagram.
     * @param opts: An Optional set of parameters to set the state of the diagram after
     *      position.
     */
    abstract position(coordSetKey: string, x: number, y: number,
                      zoom: number,
                      opts: OptionalPositionArgsI | null): void ;

    /** Position By Key
     *
     * @param modelSetKey: The model set that the disp key belongs to
     * @param dispKey: The key of the display item.
     *
     * @param coordSetKey: Optionally, which coordSet to choose, otherwise if multiple
     *                      coord sets are present, the user will be asked.
     *
     * @param opts: An Optional set of parameters to set the state of the diagram after
     *      position.
     */
    abstract positionByKey(modelSetKey: string,
                           coordSetKey: string | null,
                           opts: OptionalPositionArgsI | null): void ;

    /** Can Position By Key
     *
     * @param modelSetKey: The model set that the disp key belongs to
     * @param dispKey: The key of the display item.
     *
     * @returns A promise that fires if the position exists.
     *
     */
    abstract canPositionByKey(modelSetKey: string, dispKey: string): Promise<boolean> ;

    /** Locations For Key
     *
     * @param modelSetKey: The model set that the disp key belongs to
     * @param dispKey: The key of the display item.
     *
     * @returns A promise that fires with all the locations for that key.
     *
     */
    abstract locationsForKey(modelSetKey: string,
                             dispKey: string): Promise<DispKeyLocation[]> ;

    /** Position Updated Observable
     *
     * @return An observerable that fires when the canvas position is updated.
     */
    abstract positionUpdatedObservable(): Observable<PositionUpdatedI> ;

    /** isReady
     *
     * @returns an observable that is fired when the diagram loads a coordset
     * or the coord set changes
     */
    abstract isReadyObservable(): Observable<boolean> ;

}