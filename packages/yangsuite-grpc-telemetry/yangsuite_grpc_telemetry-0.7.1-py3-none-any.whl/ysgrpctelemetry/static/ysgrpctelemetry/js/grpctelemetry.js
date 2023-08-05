/**
 * Module for gRPC Telemetry web UI.
 */
let grpctelemetry = function() {
    "use strict";

    /**
     * Default configuration of this module.
     */
    let config = {
        /* Selector string for a progressbar */
        listenToggle: "#ys-listen-start-stop",
        listenIp: "#ys-listen-ip",
        listenPort: "#ys-listen-port",
        outputArea: "#ys-telemetry-output",
    };

    let c = config;     // internal alias for brevity

    let state = {
        listening: false,
        port: null,
        updater: null,
    }

    function getOutput() {
        const localGetUri = '/grpctelemetry/servicer/' + state.port + '/output';
        $.getJSON(localGetUri, function(data) {
            for (let block of data.output) {
                let textblock = $('<textarea readonly class="telemetry-output">');
                let newlines = block.match(/\n/g);
                let rows = (newlines ? newlines.length : 0) + 1;
                textblock.attr('rows', rows);
                textblock.val(block);
                $(c.outputArea).append(textblock);
            }
        });
    }

    function startListening() {
        let port = $(c.listenPort).val() || $(c.listenPort).attr("placeholder");
        let address = $(c.listenIp).val() || $(c.listenIp).attr("placeholder");
        const localStartUri = '/grpctelemetry/servicer/' + port + '/start'
        getPromise(localStartUri, {address: address})
            .then(function(retObj) {
                popDialog(retObj.message);
                if (!retObj.result) {
                    return;
                }
                $(c.listenToggle).text("Stop telemetry receiver");
                $(c.listenToggle).addClass("btn--negative");
                $(c.listenToggle).removeClass("btn--primary");

                state.listening = true;
                state.port = port;
                state.updater = setInterval(getOutput, 250);
            });
    };

    function stopListening(retry=10) {
        let port = state.port;
        const localStopUri = '/grpctelemetry/servicer/' + port + '/stop'
        clearInterval(state.updater);
        getPromise(localStopUri)
            .then(function(retObj) {
                if (!retObj.result && retry > 0) {
                    return stopListening(--retry);
                }
                popDialog(retObj.message);
                if (retry > 0) {
                    $(c.listenToggle).text("Start telemetry receiver");
                    $(c.listenToggle).removeClass("btn--negative");
                    $(c.listenToggle).addClass("btn--primary");
                    state.updater = null;
                    state.listening = false;
                    state.port = null;
                }
            });
    };

    function toggleListen() {
        if (state.listening) {
            stopListening();
        } else {
            startListening();
        }
    };

    /**
     * Public API.
     */
    return {
        config:config,
        toggleListen: toggleListen,
    };
}();
