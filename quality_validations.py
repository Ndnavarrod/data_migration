import great_expectations as ge

#We can increase the number of validations when we know better the informtation

def validate_input(df,table_name):
    # Initialize Great Expectations context
    
    if table_name=="hired_employees":
        columns = ['id', 'name','datetime','department_id','job_id']
        ge_df = ge.from_pandas(df)
        ge_df.expect_table_columns_to_match_ordered_list(columns)
    elif table_name=="departments":
        columns = ['id', 'department']
        ge_df = ge.from_pandas(df)
        ge_df.expect_column_values_to_be_of_type("id", "int") 
        ge_df.expect_column_values_to_be_of_type("department", "str")
        ge_df.expect_table_columns_to_match_ordered_list(columns)
    elif table_name=="jobs":
        columns = ['id', 'job']
        ge_df = ge.from_pandas(df)
        ge_df.expect_column_values_to_be_of_type("id", "int") 
        ge_df.expect_column_values_to_be_of_type("job", "str")  
        ge_df.expect_table_columns_to_match_ordered_list(columns)

    
    validation_result=ge_df.validate()
    validation_result.success

    
    return validation_result.success