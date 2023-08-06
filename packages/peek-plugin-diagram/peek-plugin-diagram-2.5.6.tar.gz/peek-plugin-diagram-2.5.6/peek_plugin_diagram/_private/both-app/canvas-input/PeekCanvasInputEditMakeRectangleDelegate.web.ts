import {
    CanvasInputPos,
    InputDelegateConstructorViewArgs,
    PeekCanvasInputDelegate
} from "./PeekCanvasInputDelegate.web";
import {EditorToolType} from "../canvas/PeekCanvasEditorToolType.web";
import {PeekCanvasEditor} from "../canvas/PeekCanvasEditor.web";
import {PointI} from "../canvas-shapes/DispBase";
import {DispRectangle} from "../canvas-shapes/DispRectangle";
import {DrawModeE} from "../canvas-render/PeekDispRenderDelegateABC.web";
import {InputDelegateConstructorEditArgs} from "./PeekCanvasInputDelegateUtil.web";

/**
 * This input delegate handles :
 * Zooming (touch and mouse)
 * Panning (touch and mouse)
 * Selecting at a point (touch and mouse)
 *
 */
export class PeekCanvasInputEditMakeRectangleDelegate extends PeekCanvasInputDelegate {
    static readonly TOOL_NAME = EditorToolType.EDIT_MAKE_RECTANGLE;

    // Stores the text disp being created
    private _creating = null;

    // Used to detect dragging and its the mouse position we use
    private _startMousePos: CanvasInputPos | null = null;


    constructor(viewArgs: InputDelegateConstructorViewArgs,
                editArgs: InputDelegateConstructorEditArgs) {
        super(viewArgs, editArgs, PeekCanvasInputEditMakeRectangleDelegate.TOOL_NAME);

        this.viewArgs.model.selection.clearSelection();
        this._reset();
    }

    _reset() {
        this._creating = null;

        // See mousedown and mousemove events for explanation
        this._startMousePos = null;
        this._lastMousePos = new CanvasInputPos();
    }


    // ============================================================================
    // Editor Ui Mouse


    // ---------------
    // Map mouse events
    mouseDown(event: MouseEvent, inputPos: CanvasInputPos) {
        this.inputStart(inputPos);
    }

    mouseMove(event: MouseEvent, inputPos: CanvasInputPos) {
        this.inputMove(inputPos);
    }

    mouseUp(event: MouseEvent, inputPos: CanvasInputPos) {
        this.inputEnd(inputPos);
    }

    // ---------------
    // Map touch events
    touchStart(event: TouchEvent, inputPos: CanvasInputPos) {
        this.inputStart(inputPos);
    };

    touchMove(event: TouchEvent, inputPos: CanvasInputPos) {
        this.inputMove(inputPos);
    };

    touchEnd(event: TouchEvent, inputPos: CanvasInputPos) {
        this.inputEnd(inputPos);
    };

    // ---------------
    // Misc delegate methods
    delegateWillBeTornDown() {
        this._finaliseCreate();
    }

    draw(ctx, zoom: number, pan: PointI, drawMode: DrawModeE) {
    }

    // ---------------
    // Start logic
    private inputStart(inputPos: CanvasInputPos) {
        this._lastMousePos = inputPos;
        if (!this._creating) {
            this._startMousePos = inputPos;
            this.createDisp(inputPos);
        }
    }

    private inputMove(inputPos: CanvasInputPos) {
        if (this._startMousePos == null)
            return;

        // if (editorUi.grid.snapping())
        //     this._creating.snap(editorUi.grid.snapSize());
        this.updateSize(inputPos);
    }


    private inputEnd(inputPos: CanvasInputPos) {
        if (!this._creating) {
            return;
        }

        this.updateSize(inputPos);

        if (!this._hasPassedDragThreshold(this._startMousePos, inputPos))
            return;

        this._finaliseCreate();
        this._reset();
    }

    private updateSize(inputPos: CanvasInputPos) {

        if (!this._creating)
            return;

        let startMouse: PointI = {x: this._startMousePos.x, y: this._startMousePos.y};
        let point: PointI = {x: inputPos.x, y: inputPos.y};
        let x = point.x < startMouse.x ? point.x : startMouse.x;
        let y = point.y < startMouse.y ? point.y : startMouse.y;

        let width = Math.abs(point.x - startMouse.x);
        let height = Math.abs(point.y - startMouse.y);

        DispRectangle.setRectanglePoint(this._creating, {x, y});
        DispRectangle.setRectangleWidth(this._creating, width);
        DispRectangle.setRectangleHeight(this._creating, height);
        this.viewArgs.config.invalidate();
    }

    private createDisp(inputPos: CanvasInputPos) {

        this._creating = DispRectangle.create(this.viewArgs.config.coordSet);

        // Link the Disp
        this.editArgs.lookupService._linkDispLookups(this._creating);

        // Add the shape to the branch
        this._creating = this.editArgs.branchContext.branchTuple
            .addOrUpdateDisp(this._creating, true);

        this.viewArgs.model.recompileModel();
        this.viewArgs.model.selection.replaceSelection(this._creating);
        this._addBranchAnchor(inputPos.x, inputPos.y);
    }

    private _finaliseCreate() {
        if (this._creating == null)
            return;

        this.editArgs.branchContext.branchTuple.touchUpdateDate(true);
        this.editArgs.branchContext.branchTuple.touchUndo();
        this.viewArgs.config.invalidate();
        this.editArgs.setEditorSelectTool();
    }
}