import click


@click.command()
@click.option('-instances', type=str,
              help='一个或多个主机ID,用空格区分')
@click.option('-image_id', type=str,
              help='一个或多个镜像ID,用空格区分')
@click.option('-instance_type', type=str,
              help='主机配置类型')
@click.option('-instance_class', type=click.Choice(['0', '1', '101', '201']),
              help='主机性能类型: 性能型:0, 超高性能型:1, 基础型:101, 企业型:201')
@click.option('-vcpus_current', type=str,
              help='主机CPU的核心数')
@click.option('-memory_current', type=str,
              help='主机内存大小')
@click.option('-os_disk_size', type=str,
              help='主机系统盘大小')
@click.option('-exclude_reserved', type=click.Choice(['0', '1']),
              help='是否过滤预留主机, 若为1, 则不返回预留主机信息')
@click.option('-status', type=click.Choice(['pending', 'running', 'stopped', 'suspended', 'terminated', 'ceased']),
              help='主机状态: pending, running, stopped, suspended, terminated, ceased')
@click.option('-search_word', type=str,
              help='搜索关键词, 支持主机ID, 主机名称')
@click.option('-tags', type=str,
              help='按照标签ID过滤, 只返回已绑定某标签的资源')
@click.option('-dedicated_host_group_id', type=str,
              help='按照专属宿主机组过滤')
@click.option('-dedicated_host_id', type=str,
              help='按照专属宿主机组中某个宿主机过滤')
@click.option('-owner', type=str,
              help='按照用户账户过滤, 只返回指定账户的资源')
@click.option('-verbose', type=click.Choice(['0', '1']),
              help='是否返回冗长的信息, 若为1, 则返回主机相关其他资源的详细数据.')
@click.option('-offset', default='0', type=str,
              help='数据偏移量, 默认为0')
@click.option('-limit', default='20', type=click.IntRange(20, 100),
              help='返回数据长度，默认为20，最大100')
@click.option('-zone', prompt='区域 ID：', type=str,
              help='主机所在的的区域ID')
def describe_instance(zone, *args, **kwargs):
    """
    获取一个或多个主机
    可根据主机ID, 状态, 主机名称, 映像ID 作过滤条件, 来获取主机列表.
    如果不指定任何过滤条件, 默认返回你所拥有的所有主机。
    """
    click.echo(f"当前区域id[{zone}]下的主机有XXX台，状态是running")


if __name__ == '__main__':
    describe_instance()
