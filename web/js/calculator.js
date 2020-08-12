const urlParams = new URLSearchParams(window.location.search);
const inputtext = document.getElementById("inputtext");
const input = document.getElementById("input");
const output = document.getElementById("output");

function evaluatecircuit() {
    console.log("Loading...");
    languagePluginLoader.then(() => {
    pyodide.loadPackage(["numpy", "micropip"]).then(()=> {
        pyodide.runPythonAsync("import micropip").then(()=>{
            pyodide.runPythonAsync("micropip.install('http://localhost:8008/parsimonious-0.8.1-py3-none-any.whl')").then(() => {
                pyodide.runPythonAsync("micropip.install('http://localhost:8008/quantum-0.1-py3-none-any.whl')").then(() => {
                    pyodide.runPythonAsync("import quantum").then(()=>{
                        console.log("Done loading");
                        console.log("Evaluating circuit...");
                        pyodide.runPython(`
                        from quantum.evaluate import evaluate
                        from quantum.grammar import parse
                        `);
                        console.log(inputtext.value);
                        pyodide.runPython("circuit = parse('" + inputtext.value + "', expand=False)");
                        pyodide.runPython("result = evaluate('"+ inputtext.value + "')");
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
                    });
                });
            })
        });
    });
};

document.getElementById('inputtext').addEventListener('keypress', function(event) {
    if (event.keyCode == 13) {
        evaluatecircuit();
    }
});

if(urlParams.get("input")) {
    console.log("Found input: " + urlParams.get("input"));
    inputtext.value = urlParams.get("input");
    evaluatecircuit();

} else {
    console.log("Loading...");
    languagePluginLoader.then(() => {
        pyodide.loadPackage(["numpy", "micropip"]).then(()=> {
            pyodide.runPythonAsync("import micropip").then(()=>{
                pyodide.runPythonAsync("micropip.install('http://localhost:8008/parsimonious-0.8.1-py3-none-any.whl')").then(() => {
                    pyodide.runPythonAsync("micropip.install('http://localhost:8008/quantum-0.1-py3-none-any.whl')").then(() => {
                        pyodide.runPythonAsync("import quantum");
                        console.log("Done loading");
                    });
                });
            })
        });
    });
}