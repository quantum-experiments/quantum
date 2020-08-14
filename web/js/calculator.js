const urlParams = new URLSearchParams(window.location.search);
const inputtext = document.getElementById("inputtext");
const input = document.getElementById("input");
const output = document.getElementById("output");
var deps = false;

function loadDeps() {
    languagePluginLoader.then(() => {
        pyodide.loadPackage(["numpy", "micropip"]).then(() => {
            pyodide.runPythonAsync("import micropip").then(() => {
                pyodide.runPythonAsync("micropip.install('http://localhost:8008/parsimonious-0.8.1-py3-none-any.whl')").then(()=> {
                    pyodide.runPythonAsync("micropip.install('http://localhost:8008/quantum-0.1-py3-none-any.whl')").then(() => {
                        console.log("Done loading");
                        deps = true;
                        evaluatecircuit();
                    });
                });
            });
        });
    });
};

function evaluatecircuit() {
    languagePluginLoader.then(() => {
        console.log("Evaluating circuit...");
        const circuit = inputtext.value.replace(/[\r\n]/g, " ");
        pyodide.runPython(`
        from quantum.evaluate import evaluate
        from quantum.grammar import parse
        `);
        console.log(circuit);
        pyodide.runPython("circuit = parse('" + circuit + "', expand=False)");
        pyodide.runPython("result = evaluate('"+ circuit + "')");
        pyodide.runPython("input = str(circuit)");
        pyodide.runPython(`
        if isinstance(result, list):
            output = ' '.join([r._repr_latex_() for r in result])
        else:
            output = result._repr_latex_()
        `);
        output.innerHTML = pyodide.globals.output;
        inputtext.innerHTML = pyodide.globals.input;
        MathJax.typeset();
        console.log(pyodide.globals.input);
        console.log(pyodide.globals.output);
        console.log("Done evaluating circuit");
    });
}

if(urlParams.get("input")) {
    console.log("Found input: " + urlParams.get("input"));
    inputtext.value = urlParams.get("input");
    if (deps == true) {
        evaluatecircuit();
    } else {
        loadDeps();
    }
}

document.getElementById('inputtext').addEventListener('keypress', function(event) {
    if(event.keyCode == 13 && event.shiftKey) {
        event.preventDefault();
        evaluatecircuit();
    }
});
