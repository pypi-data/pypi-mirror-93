import click


@click.command()
@click.option('-direct-case', default="0", type=click.Choice(["0", "1"]),
              help='是否直接彻底销毁主机，如果指定 “1” 则不会进入回收站直接销毁，默认是 “0”')
@click.option('-instances', prompt='主机id：', type=str,
              help='一个或多个主机ID,用空格区分')
@click.option('-zone', prompt='区域 ID：', type=str,
              help='主机所在的的区域ID')
def terminate_instances(direct_case, instances, zone):
    """
    销毁一台或多台主机。
    销毁主机的前提，是此主机已建立租用信息（租用信息是在创建主机成功后， 几秒钟内系统自动建立的）。
    所以正在创建的主机（状态为 pending ）， 以及刚刚创建成功但还没有建立租用信息的主机，是不能被销毁的。
    警告:已销毁的主机青云会为你保留2小时，如果误操作，请及时与我们联系。
    """
    click.echo(f"主机正在销毁中，销毁的主机的id是[{instances}], 主机所在的区域id是[{zone}]")
    if direct_case:
        click.echo(f"主机销毁完成，使用直接销毁的方式")
    else:
        click.echo(f"主机销毁完成，使用放入回收站的方式")


if __name__ == '__main__':
    terminate_instances()
