function getTextNodes() {
    var rejectScriptStyle = {
        acceptNode: function(node) {
            console.log(node.parentNode.nodeName);
            if (
                node.parentNode.nodeName !== "SCRIPT" &&
                node.parentNode.nodeName !== "STYLE"
            ) {
                return NodeFilter.FILTER_ACCEPT;
            }
        }
    };

    var walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        rejectScriptStyle,
        false
    );

    var node;
    var textNodes = [];
    while ((node = walker.nextNode())) {
        textNodes.push(node);
    }
    return textNodes;
}

function createTooltip(span, tooltipContent) {
    new Tooltip(span, {
        placement: "top",
        title: tooltipContent,
        html: true,
        delay: { show: 500, hide: 100 }
    });
}

function createTooltipContent(name, data) {
    var p = document.createElement("p");
    var title = document.createTextNode(name);
    p.appendChild(title);
    var tt = document.createElement("div");
    tt.className = "jfilter-tooltip";
    la = document.createElement("div");
    la.appendChild(document.createTextNode("LobbyAlarm 🚨"));
    tt.appendChild(la);
    tt.appendChild(p);

    var allPages = data.pages;

    if (data.hasOwnProperty("profile")) {
        allPages.unshift(data.profile);
    }

    for (var i = 0; i < allPages.length; i++) {
        var page = allPages[i];
        var a = document.createElement("a");
        var linkText = document.createTextNode(page);
        a.appendChild(linkText);
        a.title = page;
        a.href = "https://lobbypedia.de/wiki/" + page.replace(" ", "_");
        tt.appendChild(a);
        tt.appendChild(document.createElement("br"));
    }
    return tt;
}

function procNode(searchRegEx, tn) {
    var matches = [];
    while ((match = searchRegEx.exec(tn.nodeValue)) != null) {
        matches.push([match.index, match[0]]);
    }

    var offset = 0;
    for (var ii = 0; ii < matches.length; ii++) {
        var match = matches[ii];
        var replacementNode = tn.splitText(match[0] - offset);
        replacementNode.nodeValue = replacementNode.nodeValue.slice(
            match[1].length
        );
        // creating a span
        var span = document.createElement("span");
        span.className = "jfilter-highlight";
        span.appendChild(document.createTextNode(match[1] + "🚨"));

        createTooltip(span, createTooltipContent(match[1], data[match[1]]));

        // adding the span before 'bar'
        tn.parentNode.insertBefore(span, replacementNode);

        tn = replacementNode;
        offset += match[0] + match[1].length;
    }
}

(function() {
    // construct RegEx
    var searchTermsList = [];
    for (var searchTerm in data) {
        searchTermsList.push("(" + searchTerm + ")");
    }
    var searchRegEx = new RegExp(searchTermsList.join("|"), "g");

    // loop over all text nodes
    var textNodes = getTextNodes();
    var textNodesLen = textNodes.length;

    var timing = 10; // make it dynamic?
    var textNodeIndex = 0;

    function loopNode() {
        var textNode = textNodes[textNodeIndex];
        procNode(searchRegEx, textNode);

        // next
        textNodeIndex++;
        if (textNodeIndex < textNodesLen) {
            window.setTimeout(loopNode, timing);
        }
    }

    // start after 1 sec
    setTimeout(loopNode, 1000);

    console.log(textNodes);
})();
