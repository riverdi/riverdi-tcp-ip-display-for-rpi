const si = require('systeminformation');
const allthingstalk = require('allthingstalk');

allthingstalk.credentials = {
    "deviceId": "BB22LH7apDj4es6oGtKiuFXr",
    "token": "maker:4KUWJezNrHlcG0lqFzoFgLb1lTofZV2OObVeuPB"
};

allthingstalk.connect();

setInterval(function() {
    si.currentLoad(function(data) {
        allthingstalk.send (Number ((data.currentload_system).toFixed(1)), 'cpu_load');
    })
    si.cpuTemperature(function(data) {
        allthingstalk.send (Number ((data.main).toFixed(1)), 'cpu_temperature');
    })
}, 10000)