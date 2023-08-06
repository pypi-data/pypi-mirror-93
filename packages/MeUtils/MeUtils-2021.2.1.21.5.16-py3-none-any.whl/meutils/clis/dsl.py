#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : dsl
# @Time         : 2021/2/1 6:02 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *

os.environ['HADOOP_HOME'] = '/home/work/tools/infra-client/bin'
from meutils.cmds import HDFS

parser = argparse.ArgumentParser(description='ANN Serive')
parser.add_argument('--conf', default='/mipush/dsl/push_mitv/auto_debug.conf', help='zk/yaml')
args = parser.parse_args()

logger.info(f'cli args: {args.__dict__}')


class Config(BaseConfig):
    dsl_home = '/home/work/yuanjie'
    data = '/user/s_feeds/yuanjie/dsl/debug_sfile'
    biz = 'push_mitv'
    biz_conf_dir = f'{dsl_home}/dsl3/conf/{biz}'

    debug = f"{dsl_home}/dsl3/build/debug"
    libfeature = f"{dsl_home}/dsl3/libfeature.so"
    feature_group_conf = f'{dsl_home}/dsl3/conf/feature_group.conf'


conf = Config.parse_yaml(args.conf) if Path(args.conf).is_file() else Config.parse_zk(args.conf)

# git_pull
git_pull(f"{conf.dsl_home}/dsl3")
git_pull(f"{conf.dsl_home}/build-index")

# build
magic_cmd(f"cd {conf.dsl_home}/dsl3 && sh {conf.dsl_home}/dsl3/release.sh")
magic_cmd(f"cd {conf.dsl_home}/build-index && mvn package")

# data => bin_data
debug_dir = f"{conf.dsl_home}/{conf.biz}_dsl_debug"

# Path(debug_dir).mkdir(parents=True, exist_ok=True)
magic_cmd(f'mkdir {debug_dir}')
if HDFS.check_path_isexist(f'{conf.data}/part-00000'):
    HDFS.magic_cmd(f'-get -f {conf.data}/part-00000 {debug_dir}/data.sfile')

magic_cmd(f"cd {debug_dir} && {conf.dsl_home}/build-index/script/run.sh --impression data.sfile && ls")

# debug.conf
debug_conf = f"""
--conf={conf.biz_conf_dir}
--feature_group={conf.feature_group_conf}
--data_dir={debug_dir}
--trace_id=
--item_id=
--features=age
"""
with open(f'{debug_dir}/debug.conf', 'w') as f:
    f.write(debug_conf)

magic_cmd(f'{conf.debug} {debug_dir}/debug.conf')


def main():
    pass


if __name__ == '__main__':
    main()
