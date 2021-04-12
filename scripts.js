
tf.loadLayersModel("model/model.json").then(function(model) {
    window.model = model;
});

function generate(){
    document.getElementById("name").value = 'my model output';
}

function copy(){
    var text = document.getElementById('name');
    text.select();
    text.setSelectionRange(0, 99999); /* For mobile devices */
    document.execCommand("copy");
    /* Alert the copied text */
    alert("Name copied!");
}
