let aglio = require('aglio');

// Render blueprint to html

const options = {
  themeVariables: 'default'
};


const documentation_output = './app/templates/documentation.html';
const documentation_input = './APIBlueprint/blueprint.md';

aglio.renderFile(documentation_input, documentation_output, options, function (err, warnings) {
    if (err) return console.log(err);
    // if (warnings) console.log(warnings);
    console.log('documentation.html successfully dumped in ' + documentation_output);
});
