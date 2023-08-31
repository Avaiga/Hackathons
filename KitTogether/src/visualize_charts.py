def visualizing_errors(errors_array, contrast_errors_array, alerts_array):
    
    # Errors

    typeOfError = []
    numberOfErrors = []

    for error in errors_array:
        typeOfError.append(error["id"])
        numberOfErrors.append(error["count"])

    for error in contrast_errors_array:
        typeOfError.append(error["id"])
        numberOfErrors.append(error["count"])

    dataErrors = {
        "Type of Error": typeOfError,
        "Number of Errors": numberOfErrors
    }

    # Alerts

    typeOfAlert = []
    numberOfAlerts = []

    for alert in alerts_array:
        typeOfAlert.append(alert["id"])
        numberOfAlerts.append(alert["count"])

    dataAlerts = {
        "Type of Alert": typeOfAlert,
        "Number of Alerts": numberOfAlerts
    }

    return dataErrors, dataAlerts