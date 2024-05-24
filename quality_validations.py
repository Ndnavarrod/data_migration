import great_expectations as ge

#We can increase the number of validations when we know better the informtation

def validate_input(df,table_name):
    # Initialize Great Expectations context
    
    if table_name=="hired_employees":
    
        df.columns = ['id', 'name','datetime','department_id','job_id']
        ge_df = ge.from_pandas(df)
        ge_df.expect_column_values_to_be_of_type("id", "int64") 
        ge_df.expect_column_values_to_be_of_type("name", "object")  
        ge_df.expect_column_values_to_be_of_type("datetime", "object")  
        ge_df.expect_column_values_to_match_regex("department_id", "^-?\\d+$|^-?\\d+\\.\\d+$")
        ge_df.expect_column_values_to_match_regex("job_id", "^-?\\d+$|^-?\\d+\\.\\d+$") 

        #ge_df.expect_table_columns_to_match_ordered_list(columns)
    elif table_name=="deparments":
        df.columns = ['id', 'deparment']
        ge_df = ge.from_pandas(df)
        #ge_df.expect_table_columns_to_match_ordered_list(columns)
    elif table_name=="jobs":
        df.columns = ['id', 'job']
        ge_df = ge.from_pandas(df)
        ge_df.expect_column_values_to_be_of_type("id", "int64") 
        ge_df.expect_column_values_to_be_of_type("deparment", "object")  


    
    validation_result=ge_df.validate()
    validation_result.success
    print(validation_result)
    
    return validation_result.success