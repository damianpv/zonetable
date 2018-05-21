/*jslint  browser: true, white: true, plusplus: true */
/*global $: true */

$(function () {
    'use strict';

    // Load countries then initialize plugin:
    $.ajax({
        url: '/get_restaurant/',
        dataType: 'json'
    }).done(function (source) {
        var restaurant = $.map(source, function (value, key) { 
            return { value: source[key]["fields"]["title"], data: 0 }; 
        });

        // Setup jQuery ajax mock:
        /*$.mockjax({
            url: '*',
            responseTime: 200,
            response: function (settings) {
                var query = settings.data.query,
                    queryLowerCase = query.toLowerCase(),
                    suggestions = $.grep(countries, function(country) {
                         return country.toLowerCase().indexOf(queryLowerCase) !== -1;
                    }),
                    response = {
                        query: query,
                        suggestions: suggestions
                    };

                this.responseText = JSON.stringify(response);
            }
        });*/

        // Initialize ajax autocomplete:
        /*$('#id_Nombre').autocomplete({
            serviceUrl: '/autosuggest/service/url',
            onSelect: function(suggestion) {
                $('#selction-ajax').html('You selected: ' + suggestion.value + ', ' + suggestion.data);
            }
        });*/

        // Initialize autocomplete with local lookup:
        $('#id_Nombre').autocomplete({
            lookup: restaurant,
            onSelect: function (suggestion) {
                //$('#selction-ajax').html('You selected: ' + suggestion.value + ', ' + suggestion.data);
            }
        });
        
        // Initialize autocomplete with custom appendTo:
        $('#autocomplete-custom-append').autocomplete({
            lookup: restaurant,
            appendTo: '#suggestions-container'
        });
    });
});