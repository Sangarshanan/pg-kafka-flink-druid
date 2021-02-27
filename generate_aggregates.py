# docker-compose exec jobmanager bash

from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, DataTypes, EnvironmentSettings
env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(stream_execution_environment=env)
t_env.get_config().get_configuration().set_boolean("python.fn-execution.memory.managed", True)


def generate_aggregates():
    register_postgres = """
    CREATE CATALOG postgres WITH (
        'type'='jdbc',
        'property-version'='1',
        'base-url'='jdbc:postgresql://postgres:5432/',
        'default-database'='postgres',
        'username'='postgres',
        'password'='postgres'
    )
    """
    t_env.execute_sql(register_postgres)
    t_env.execute_sql("USE CATALOG postgres")
    t_env.execute_sql("SHOW tables")

    source_ddl = """
    CREATE TABLE default_catalog.default_database.test
    WITH (
    'connector' = 'kafka',
    'topic' = 'dbserver1.public.test',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'test-consumer-group',
    'format' = 'debezium-json',
    'scan.startup.mode' = 'earliest-offset'
    )
    LIKE `public.test` (
    EXCLUDING OPTIONS)
    """
    t_env.execute_sql(source_ddl)

    t_env.execute_sql("USE CATALOG default_catalog")
    t_env.execute_sql("SHOW tables") # test should show up

    # t_env.execute_sql("select * from test")

    sink_ddl = """
    CREATE TABLE test_sink (
        `name` VARCHAR(50),
        `value` INT
    ) with (
    'connector' = 'kafka',
    'topic' = 'sink',
    'properties.bootstrap.servers' = 'kafka:9092'
    )
    """
    t_env.execute_sql(sink_ddl)

    t_env.execute_sql("""
    INSERT INTO test_sink
    select name,`value` from test
    """)

    # t_env.from_path('test').select("name, value").group_by("name").select("name, sum(value)").execute_insert('test_sink')

if __name__ == '__main__':
    generate_aggregates()

