import domainlist from "./domain_list.js";


chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
  if(!tab) return;
  if (changeInfo.status != 'complete' || !tab.url.includes('video')){return; }
    
  chrome.tabs.executeScript(tabId, {file: "script.js"}, function(){});

 setTimeout(() => {
    var content = '';
    let domain = getDomain(tab.url);

    chrome.cookies.getAll({}, function(cookies) {
      for (let i in cookies) {
        let cookie = cookies[i]; 
        if (cookie.domain.indexOf(domain) != -1) {  
          if (cookie['name'] == 'Authorization_Api' || cookie['name'] == 'Signature_Api'){
            content +=  cookie['name'].substring(0, cookie['name'].length-4) + '=' + cookie['value'] + ';';
          }
          else if (cookie['name'] == 'ampURL'){
            var bkg = chrome.extension.getBackgroundPage();
            bkg.console.log(cookies['value'])
            content += cookie['value'] + ';';
          }
        }
      }
  
      let blob = new Blob([content], {type: 'text/plain'});
      let objectURL = URL.createObjectURL(blob);

      chrome.storage.local.get(["overwrite"], function(item) {
        let downloadOptions = {
          "url": objectURL,
          "filename": "cookies"
        };

        if(item.overwrite) {
          downloadOptions["conflictAction"] = "overwrite"
        }

        chrome.downloads.download(downloadOptions)
      });
    });

 }, 5000);
  
});


function escapeForPre(text) {
  return String(text).replace(/&/g, "&amp;")
                     .replace(/</g, "&lt;")
                     .replace(/>/g, "&gt;")
                     .replace(/"/g, "&quot;")
                     .replace(/'/g, "&#039;");
}

function getDomain(url) {
  let server = url.match(/:\/\/(.[^/:#?]+)/)[1];
  let parts = server.split(".");
  let domain = "";

  let isIp = !isNaN(parseInt(server.replace(".",""), 10));

  if (parts.length <= 1 || isIp) {
    domain = server;
  }
  else {
    //search second level domain suffixes
    let domains = new Array();
    domains[0] = parts[parts.length - 1];
    for(let i = 1; i < parts.length; i++) {
      domains[i] = parts[parts.length - i - 1] + "." + domains[i - 1];
      if (!domainlist.hasOwnProperty(domains[i])) {
        domain = domains[i];
        break;
      }
    }

    if (typeof(domain) == "undefined") {
      domain = server;
    }
  }
  
  return domain;
}