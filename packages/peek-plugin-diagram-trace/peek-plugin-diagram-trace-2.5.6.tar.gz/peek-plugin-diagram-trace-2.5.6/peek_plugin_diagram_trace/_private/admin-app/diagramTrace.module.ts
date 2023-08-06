import {CommonModule} from "@angular/common";
import {FormsModule} from "@angular/forms";
import {NgModule} from "@angular/core";
import {Routes, RouterModule} from "@angular/router";
import {EditSettingComponent} from "./edit-setting-table/edit.component";


// Import our components
import {DiagramTraceComponent} from "./diagramTrace.component";

// Define the routes for this Angular module
export const pluginRoutes: Routes = [
    {
        path: '',
        component: DiagramTraceComponent
    }

];

// Define the module
@NgModule({
    imports: [
        CommonModule,
        RouterModule.forChild(pluginRoutes),
        FormsModule
    ],
    exports: [],
    providers: [],
    declarations: [DiagramTraceComponent, EditSettingComponent]
})
export class DiagramTraceModule {

}
