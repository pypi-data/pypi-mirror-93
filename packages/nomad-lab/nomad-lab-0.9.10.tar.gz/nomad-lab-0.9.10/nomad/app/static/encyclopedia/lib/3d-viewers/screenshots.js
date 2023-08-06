"use strict";
const structureviewer_1 = require("./structureviewer");
const loadutils_1 = require("./loadutils");
// Function for saving screenshots from files in a folder
// When given a path to a folder, this function will search for a file named
// "norm_files.json". That file should contain a JSON list o filepaths that
// will be loaded. Next, the found filenames are searched within the given
// folder. If a file is found, that system from that file is loaded and
// visualized, and a screenshot is saved.
function saveScreenshots(folder) {
    let paths = [];
    let filenames;
    let filelist = folder + "screenshot_list.json";
    loadutils_1.loadJSON(filelist, function (filenames) {
        // Create the viewer
        let targetElement = document.getElementById("visualizationCanvas");
        let viewer = new structureviewer_1.StructureViewer(targetElement, true);
        // Visualize the data from each file wth the same viewer
        for (let i = 0; i < filenames.length; ++i) {
            //for (let i=0; i < 5; ++i) {
            let filename = filenames[i];
            let filepath = folder + filename;
            let result;
            loadutils_1.loadJSON(filepath, function (data) {
                viewer.load(data);
                viewer.takeScreenShot(filename.slice(0, -5));
            }, loadutils_1.loadError);
        }
    }, loadutils_1.loadError);
}
//============================================================================
// Save screenshots from data in folder
let dir = "data/systems/";
saveScreenshots(dir);
