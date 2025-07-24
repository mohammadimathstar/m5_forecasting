from codes.reporting import prepare_reference_data, calculate_metrics


def test_prepare_reference_data_runs(sample_input_df):
    ds = prepare_reference_data(sample_input_df)
    print(ds)
    assert ds is not None


def test_calculate_metrics_output_format(sample_input_df):
    reference_ds = prepare_reference_data(sample_input_df)
    current_batch = sample_input_df
    current_batch["d"] = "d_1850"
    print("hh", current_batch)

    result = calculate_metrics(reference_ds, current_batch, day_index=1850)
    assert isinstance(result, dict)
    assert "prediction_drift" in result
