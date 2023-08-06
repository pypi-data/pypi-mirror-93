library(methods)
library(gbm)
library(jsonlite)
library(caret)

initialise_model <- function() {
    print("Loading model...")
    model <- readRDS("artifacts/input/model.rds")
}

evaluate <- function(data_conf, model_conf, ...) {
    model <- initialise_model()

    # implement evaluatiuon

    # write(jsonlite::toJSON(metrics, auto_unbox = TRUE, null = "null", keep_vec_names=TRUE), "artifacts/output/metrics.json")
}

score.restful <- function(model, data, ...) {
    print("Scoring model...")

    # implement if resetful model serving
}

score.batch <- function(data_conf, model_conf, model_version, ...) {
    print("Batch scoring model...")

    # implement if resetful model serving

}