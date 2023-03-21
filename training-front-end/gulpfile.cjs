const uswds = require("@uswds/compile");

uswds.settings.version = 3;

uswds.paths.dist.img = "./public/images";
uswds.paths.dist.fonts = "./public/fonts";
uswds.paths.dist.js = "./public/js";
uswds.paths.dist.css = "./src/styles/uswds";

exports.init = uswds.init;
exports.update = uswds.updateUswds;
exports.compile = uswds.compile;
exports.watch = uswds.watch;
exports.default = uswds.watch;
