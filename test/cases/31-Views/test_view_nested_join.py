from new_test_framework.utils import tdLog, tdSql, sc, clusterComCheck, cluster, sc, clusterComCheck


class TestViewNestedJoin:

    def setup_class(cls):
        tdLog.debug(f"start to execute {__file__}")

    def test_view_nested_join(self):
        """带嵌套查询的复杂视图

        1. 创建普通表、子表
        2. 创建包含嵌套查询的复杂视图
        3. 查询视图

        Catalog:
            - View

        Since: v3.0.0.0

        Labels: common,ci

        Jira: None

        History:
            - 2025-4-28 Simon Guan Migrated from tsim/query/nestedJoinView.sim

        """

        tdSql.prepare("test", drop=True)

        tdSql.execute(
            f"CREATE TABLE `resource_info` ( job_id_ts TIMESTAMP , role VARCHAR(20) primary key, start_time TIMESTAMP, ip VARCHAR(15), cpu FLOAT, memory FLOAT, io_write FLOAT, io_read FLOAT, net_write FLOAT, net_read FLOAT) TAGS ( end_time TIMESTAMP);"
        )
        tdSql.execute(
            f"CREATE STABLE `test_results` (   `job_id_ts` TIMESTAMP ,   `end_time` VARCHAR(40)  PRIMARY KEY,  `job_id` BIGINT,  `time_cost` FLOAT,  `write_speed` FLOAT,   `qps` FLOAT,  `min_delay` FLOAT,   `p90_delay` FLOAT,   `p95_delay` FLOAT,   `p99_delay` FLOAT,  `max_delay` FLOAT,  `avg_delay` FLOAT,  `hostname` VARCHAR(15),  `tdengine_commit_id` VARCHAR(50),  `tdinternal_commit_id` VARCHAR(50),   `load_type` VARCHAR(50),  `cpu` FLOAT,  `memory` FLOAT,  `io_write` FLOAT,   `io_read` FLOAT)  TAGS ( `branch` VARCHAR(50),  `scenario` VARCHAR(50),  `test_case` VARCHAR(1000),  `env_id` INT,  `type` VARCHAR(50));"
        )
        tdSql.execute(
            f"CREATE TABLE `job_info` ( `start_time` TIMESTAMP ,  `finish_time` TIMESTAMP ,   `job_id` INT,  `job_status` VARCHAR(20), `test_type` VARCHAR(50),   `environment` INT,  `version` VARCHAR(20),  `tdengine_commit_id` VARCHAR(50),  `tdinternal_commit_id` VARCHAR(50),  `type` VARCHAR(50),   `scenario` VARCHAR(50),  `note` VARCHAR(500), `version_number` VARCHAR(20));"
        )
        tdSql.execute(
            f"create view abc as select * from (  select   a.job_id,  a.start_time as  job_start_time,  a.finish_time as job_end_time,  a.job_status,  a.test_type,  a.environment,  case when a.version_number <> null then a.version else CONCAT(a.version,'_',a.version_number) end as version_info, a.tdengine_commit_id,  a.tdinternal_commit_id,  a.type,  a.scenario,  a.note,  a.version_number, b.end_time as tc_end_time, b.time_cost, b.write_speed, b.qps, b.min_delay, b.p90_delay, b.p95_delay, b.p99_delay, b.`max_delay`, b.avg_delay, b.hostname, b.load_type, b.scenario, b.test_case, b.type  from job_info a, test_results b  where a.start_time=b.job_id_ts  and a.job_status='finished') s1 inner join resource_info s2 on s1.job_start_time=s2.job_id_ts and s1.job_id=2 and s1.tc_end_time=s2.end_time;"
        )
        tdSql.query(f"select * from abc;")
