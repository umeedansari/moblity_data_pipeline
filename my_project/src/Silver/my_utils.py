from pyspark.sql.functions import *
from pyspark.sql.window import Window
from typing import List
from pyspark.sql import DataFrame
from delta.tables import DeltaTable

class transformation():
    def dedup(self, df: DataFrame, dedup_key: List[str], cdc: str) -> DataFrame:
        window_spec = Window.partitionBy(*dedup_key).orderBy(col(cdc).desc())
        df = df.withColumn("row_number", row_number().over(window_spec))
        df = df.filter(col("row_number") == 1).drop("row_number")
        return df

    def process_date(self, df: DataFrame) -> DataFrame:
        return df.withColumn('process_date', current_timestamp())
    
    def upsert(self,df:DataFrame,key_cols:List,table,cdc):
        condition=[f'trg.{k} = src.{k}' for k in key_cols]
        final_cond=' and '.join(condition)
        trg_df=DeltaTable.forName(spark,f'Project2.silver.{table}')
        trg_df.alias("trg").merge(df.alias("src"),final_cond)\
                            .whenMatchedUpdateAll(condition=f'src.{cdc} > trg.{cdc}')\
                            .whenNotMatchedInsertAll()\
                            .execute()
        