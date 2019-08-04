async function search() {
  let qr = document.getElementById('query');
  let response = await fetch(`http://10.105.17.11:5001/?q=${query.value}`);
  let data = await response.json();
  if(data['query_parts']) {
    delete data['query_parts'];
  }
  if(data['t']) {
    data['t'].forEach((each,id)=>{
      if(each['translate']) {
        delete each['translate'];
      }
      if(each['r_type']) {
        delete each['r_type'];
      }
      if(each['type']) {
        delete each['type'];
      }
    })
  }
  $('#jsonOutput').jsonViewer(data);
  es(data);
}


function es(data) {


    fetch('http://10.105.16.254:9200/dataframe3/_search', {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then(res=>res.json())
      .then(res => {
        let eachResult = res['hits']['hits'];
        results.forEach((eachResult, idx) => {

          let config = eachResult.config;
          config.description = config.description || '';
          let template = `
              <div class="col-md">
                <div class="row">
                  <div class="col-md" style="max-width:300px;">
                    <img src="${eachResult.thumbnail || eachResult.images[0]}" height="200" width="250" />
                  </div>
                  <div class="col-md">
                    <div><h3><a href="/results.html?q=${eachResult.name}">${eachResult.name}</a> </h3></div>
                    <div class="row">
                        <div class="col-md"><b>Price: </b>${config.available_price}</div>
                        <div class="col-md"><b>Brand: </b>${config.brand}</div>
                        <div class="col-md"><b>Category: </b>${config.category}</div>
                        <div class="col-md"><b>Subcategory: </b>${config.subcategory}</div>
                    </div>
                    <br/>
                    <div>${config.description.substring(0,200)}...</div>
                    </div>
                  </div>
                </div>
              </div>
              <br/>
              <hr/>
          `;
          renderResults.push(template);
        });
        let output = `
                  <br/>
                  <div> <b>Total Results:</b> ${totalResults} </div>
                  <br/>
                  <div clas="row">
                    ${renderResults.join(' ')}
                  </div>
        `;

        document.getElementById('searchResults').innerHTML = output;
      });

}
