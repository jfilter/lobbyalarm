!function(){"use strict";var e="undefined"==typeof global?self:global;if("function"!=typeof e.require){var r={},n={},t={},i={}.hasOwnProperty,o=/^\.\.?(\/|$)/,u=function(e,r){for(var n,t=[],i=(o.test(r)?e+"/"+r:r).split("/"),u=0,s=i.length;u<s;u++)n=i[u],".."===n?t.pop():"."!==n&&""!==n&&t.push(n);return t.join("/")},s=function(e){return e.split("/").slice(0,-1).join("/")},l=function(r){return function(n){var t=u(s(r),n);return e.require(t,r)}},a=function(e,r){var t=w&&w.createHot(e),i={id:e,exports:{},hot:t};return n[e]=i,r(i.exports,l(e),i),i.exports},c=function(e){return t[e]?c(t[e]):e},f=function(e,r){return c(u(s(e),r))},d=function(e,t){null==t&&(t="/");var o=c(e);if(i.call(n,o))return n[o].exports;if(i.call(r,o))return a(o,r[o]);throw new Error("Cannot find module '"+e+"' from '"+t+"'")};d.alias=function(e,r){t[r]=e};var p=/\.[^.\/]+$/,_=/\/index(\.[^\/]+)?$/,v=function(e){if(p.test(e)){var r=e.replace(p,"");i.call(t,r)&&t[r].replace(p,"")!==r+"/index"||(t[r]=e)}if(_.test(e)){var n=e.replace(_,"");i.call(t,n)||(t[n]=e)}};d.register=d.define=function(e,t){if(e&&"object"==typeof e)for(var o in e)i.call(e,o)&&d.register(o,e[o]);else r[e]=t,delete n[e],v(e)},d.list=function(){var e=[];for(var n in r)i.call(r,n)&&e.push(n);return e};var w=e._hmr&&new e._hmr(f,d,r,n);d._cache=n,d.hmr=w&&w.wrap,d.brunch=!0,e.require=d}}(),function(){var e;"undefined"==typeof window?this:window;require.register("js/initialize.js",function(e,r,n){"use strict";function t(e){return e&&e.__esModule?e:{"default":e}}var i=r("./someFile"),o=t(i);document.addEventListener("DOMContentLoaded",function(){console.log("initialized"),(0,o["default"])()})}),require.register("js/someFile.js",function(e,r,n){"use strict";function t(){console.log("some function")}Object.defineProperty(e,"__esModule",{value:!0}),e["default"]=t}),require.alias("process/browser.js","process"),e=require("process"),require.register("___globals___",function(e,r,n){window.jQuery=r("jquery"),window.$=r("jquery"),window.bootstrap=r("bootstrap")})}(),require("___globals___"),require("js/initialize");