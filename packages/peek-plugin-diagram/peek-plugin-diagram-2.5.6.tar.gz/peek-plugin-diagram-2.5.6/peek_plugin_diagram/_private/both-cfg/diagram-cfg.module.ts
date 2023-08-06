import { CommonModule } from "@angular/common";
import { HttpClientModule } from "@angular/common/http";
import { NgModule } from "@angular/core";
import { Routes } from "@angular/router";
import { FormsModule } from "@angular/forms";
import { NzIconModule } from "ng-zorro-antd/icon";
import { RouterModule } from "@angular/router";
import { DiagramCfgComponent } from "./diagram-cfg.component";

// Define the child routes for this plugin.
export const pluginRoutes: Routes = [
    // {
    //     path: 'showDiagram',
    //     component: DiagramCfgComponent
    // },
    {
        path: "",
        pathMatch: "full",
        component: DiagramCfgComponent,
    },
];

// Define the root module for this plugin.
// This module is loaded by the lazy loader, what ever this defines is what is started.
// When it first loads, it will look up the routes and then select the component to load.
@NgModule({
    imports: [
        CommonModule,
        RouterModule.forChild(pluginRoutes),
        FormsModule,
        HttpClientModule,
        NzIconModule,
    ],
    exports: [],
    providers: [],
    declarations: [DiagramCfgComponent],
})
export class DiagramCfgModule {}
