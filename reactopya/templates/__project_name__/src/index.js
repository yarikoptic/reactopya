import React from "react";
import ReactDOM from "react-dom";
import MainWindow from "./components/MainWindow";
const config = require('../reactopya.config.json');

const ReactopyaClient = require('./ReactopyaClient');

const show_main_window = () => {
    if (!window.using_electron) {
        window.reactopya_client = new ReactopyaClient();
        window.reactopya_client.connect(`ws://${window.location.host}`);
    }

    setTimeout(function() {
        ReactDOM.render((
            <MainWindow config={config} />
        ),
            document.getElementById("root")
        );
    }, 500);
    
};

show_main_window();