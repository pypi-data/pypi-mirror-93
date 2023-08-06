// ============================================================================
// Editor Ui Mouse

import {PeekCanvasInput} from "./PeekCanvasInput.web";
import {PeekCanvasConfig} from "../canvas/PeekCanvasConfig.web";
import {PeekCanvasModel} from "../canvas/PeekCanvasModel.web";
import {PeekDispRenderFactory} from "../canvas-render/PeekDispRenderFactory.web";
import {PeekCanvasEditorProps} from "../canvas/PeekCanvasEditorProps";
import {PrivateDiagramLookupService} from "@peek/peek_plugin_diagram/_private/services/PrivateDiagramLookupService";
import {PrivateDiagramBranchContext} from "@peek/peek_plugin_diagram/_private/branch/PrivateDiagramBranchContext";
import {DocDbPopupService} from "@peek/peek_plugin_docdb";
import {PeekCanvasActioner} from "../canvas/PeekCanvasActioner";


export function disableContextMenu(event) {
    event.preventDefault();
    return false;
}

export class CanvasInputPos {
    x: number = 0;
    y: number = 0;
    clientX: number = 0;
    clientY: number = 0;
    time: Date = new Date();
}

export class CanvasInputDeltaI {
    dx: number = 0;
    dy: number = 0;
    dClientX: number = 0;
    dClientY: number = 0;
}

export interface InputDelegateConstructorViewArgs {
    input: PeekCanvasInput;
    config: PeekCanvasConfig;
    model: PeekCanvasModel;
    renderFactory: PeekDispRenderFactory;
    objectPopupService: DocDbPopupService;
    actioner: PeekCanvasActioner;
}

export interface InputDelegateConstructorEditArgs {
    setEditorSelectTool: () => void;
    doUndo: () => void;
    doRedo: () => void;
    branchContext: PrivateDiagramBranchContext;
    editToolbarProps: PeekCanvasEditorProps;
    lookupService: PrivateDiagramLookupService;
}
