var idValid = false;
var defaultMsg = "This name has to be unique within the project and can ONLY contain alphanumeric (0-9, a-z, A-Z) and underscore character.";

function initializeIdValidations(idElement, submitBtnSelector) {
    $(document).ready(function() {
        appendIdHelpText(idElement);
        registerIdForValidation(idElement, submitBtnSelector);
    });
}

function appendIdHelpText(selector) {
    var helpText = '<small class="form-text text-muted float-left"></small>';
    $(selector).after(helpText);
    setHelpText(defaultMsg);
}

function registerIdForValidation(idElement, submitButtonSelector) {
    $(idElement).change(function(event) {
        validateId(event, this, submitButtonSelector);
    });
}

function setHelpText(content) {
    $(".form-text.text-muted").text(content);
}

function helpTextHighlight() {
    $(".form-text.text-muted").addClass("red-font");
}

function helpTextLowlight() {
    $(".form-text.text-muted").removeClass("red-font");
}

function enableButton(btnSelector) {
    $(btnSelector).removeClass("disabled").prop("disabled", false);
}

function disableButton(btnSelector) {
    $(btnSelector).addClass("disabled").prop("disabled", true);
}

function validateId(event, inputElement, submitButtonSelector) {
    var currentId = $(inputElement).val();
    var isValid = false;
    var isDuplicate = true;

    if(currentId.length > 0) {
    	var pattern = /^\w+$/;
        var existingIds = $(inputElement).data("values").split(",");
        isDuplicate = ($.inArray(currentId, existingIds) != -1);
        isValid = pattern.test(currentId);
    }
    idValid = isValid && !isDuplicate;
    if(!idValid) {
        $(inputElement).parent("div").addClass("has-error");
        disableButton(submitButtonSelector);
        helpTextHighlight();
    } else {
        $(inputElement).parent("div").removeClass("has-error");
        enableButton(submitButtonSelector);
        helpTextLowlight();
    }
}