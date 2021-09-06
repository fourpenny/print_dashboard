/*
 * View model for print_dashboard
 *
 * Author: Christian Clark
 * License: AGPLv3
 */
$(function() {
  function Print_dashViewModel(parameters) {
     var self = this;
     //self.baseUrl = OctoPrintClient.getBaseUrl();
     self.message = ko.observable("hello")

     self.getData = function () {
       $.ajax({
         type: 'GET',
         dataType: 'json',
         success: self.updateData,
         url: self.baseUrl + '/api/plugin/print_dash?data='+ 'successful_prints'
         //successful_prints will be a variable, just need to make sure implementation works first
       });
     };

     /* view model class, parameters for constructor, container to bind to
      * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
      * and a full list of the available options.
      */
    }
    OCTOPRINT_VIEWMODELS.push({
        construct: Print_dashViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_print_dash, #tab_plugin_print_dash, ...
        elements: ['#tab_plugin_print_dash']
    });
});
