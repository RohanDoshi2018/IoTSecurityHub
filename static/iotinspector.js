function device(n, pswd, priv, bhr) {
	this.name = n;
	this.password = pswd;
	this.privacy = priv;
	this.behavior = bhr;
}

function icon(i) {
	if (i === 1) return "ok";
	else return "remove";
}

function color(i) {
	if (i === 1) return "green";
	else return "red";
}

function openInfo() {

}

function makeTag(device) {
	var name = device.name;
	var pass = device.password;
	var priv = device.privacy;
	var bhvr = device.behavior;

	// result = document.getElementById("panels").innerHTML;
    result = "<div class='panel panel-default' style='height: 100px'>" + 
      "<div style='float: left; width: 40%'>" + 
        "<h3 style='margin-left: 20px'>" + name + "</h3>" +
      "</div>" +

      "<div style='float: left; width: 20%'>" + 
        "<div class='panel-body'>Password</div>" +
        "<button id='" + name + 1 + "' type='button' class='btn btn-default btn-circle btn-xl btn-info' style='margin-left: 20px;background:" + color(pass) + ";color:white' data-toggle='modal' data-target='#passModal" + pass + "'><i class='glyphicon glyphicon-" + icon(pass) + "'></i></button>" +
      "</div>" +

      "<div style='float: left; width: 20%'>" +
        "<div class='panel-body'>Privacy</div>" +
        "<button id='" + name + 2 + "' type='button' class='btn btn-default btn-circle btn-xl btn-info' style='margin-left: 20px;background:" + color(priv) + ";color:white' data-toggle='modal' data-target='#privModal" + priv + "'><i class='glyphicon glyphicon-" + icon(priv) + "'></i></button>" +
      "</div>" +
 
      "<div style='float: left; width: 20%'>" +
        "<div class='panel-body'>Behavior</div>" +
        "<button id='" + name + 3 + "' type='button' class='btn btn-default btn-circle btn-xl btn-info' style='margin-left: 20px;background:" + color(bhvr) + ";color:white' data-toggle='modal' data-target='#bhvrModal" + bhvr + "'><i class='glyphicon glyphicon-" + icon(bhvr) + "'></i></button>" +
      "</div>" +
    "</div>";
    return result
}

function showDevices(devices) {
	results = "";
	for (var i = 0; i < devices.length; i++) {
		results += makeTag(devices[i])
	}
	document.getElementById("panels").innerHTML = results;
}

function makeDeviceList () {
	var devices = [];

	bpm = new device("Withings Blood Pressure Monitor", 1, 1, 1);
	scale = new device("1byOne Smart Scale", 1, 0, 1);
	blood = new device("iHeart Blood Sugar Monitor", 0, 1, 1);
	bpm2 = new device("iHearth Blood Pressure Sytem", 0, 1, 0);
	scale2 = new device("Withings Smart Scale", 1, 1, 1);
	nest = new device("Nest Camera", 1, 1, 0);

	devices.push(bpm);
	devices.push(scale);
	devices.push(blood);
	devices.push(bpm2);
	devices.push(scale2);
	devices.push(nest);

	showDevices(devices);

	bpm = new device("Withings Blood Pressure Monitor", 0, 0, 0);
	devices[0] = bpm;
	showDevices(devices);
}
