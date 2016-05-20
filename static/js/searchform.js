"use strict";

var searchForm = document.getElementById('srch-ticker');

function flakySearch(evt) {
    alert("I don't feel like searching");
    evt.preventDefault();
    }

searchForm.addEventListener('submit', flakySearch);