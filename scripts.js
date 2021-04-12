
tf.loadLayersModel("model/model.json").then(function(model) {
    window.model = model;
});


async function load(){
    const model = await tf.loadLayersModel('model/model.json');
    return model.summary()
  };
//var loadedModel = await tf.loadLayersModel('https://github.com/aliswh/fantasy-name-generator/blob/main/model/model.json');

function predict(model) {
    const model = load();
    const tensor = tf.tensor();
    model.then(model => {
        let result = model.predict(tensor);
        result = result.dataSync()[0];
        return result;
    });
};

function generate(){
    document.getElementById("name").value = predict();
};

function copy(){
    var text = document.getElementById('name');
    text.select();
    text.setSelectionRange(0, 99999); /* For mobile devices */
    document.execCommand("copy");
    /* Alert the copied text */
    alert("Name copied!");
};
