function storeData() {
    fetch('/store', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({dataHash: 'sampleHash', nodeId: 'node1'})
    }).then(response => response.json())
      .then(data => console.log(data));
}
