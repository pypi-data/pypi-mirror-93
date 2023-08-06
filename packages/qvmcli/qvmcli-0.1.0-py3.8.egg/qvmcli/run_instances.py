import click


@click.command()
@click.option('-image_id', prompt='映像ID：', type=str,
              help='映像ID，此映像将作为主机的模板。可传青云提供的映像ID，或自己创建的映像ID')
@click.option('-instance_type', type=str,
              help='主机类型，')
@click.option('-cpu', type=click.Choice(['1', '2', '4', '8', '16']),
              help='CPU core，有效值为: 1, 2, 4, 8, 16')
@click.option('-memory',
              type=click.Choice(['1024', '2048', '4096', '6144', '8192', '12288', '16384', '24576', '32768']),
              help='内存，有效值为: 1024, 2048, 4096, 6144, 8192, 12288, 16384, 24576, 32768')
@click.option('-os_disk_size', type=str,
              help='系统盘大小，单位GB。Linux操作系统的有效值为：20-100，默认值为：20; '
                   'Windows操作系统的有效值为：50-100，默认值为：50')
@click.option('-count', type=str, default="1",
              help='创建主机的数量，默认是1')
@click.option('-instance_name', type=str,
              help='主机名称')
@click.option('-login_mode', type=click.Choice(['keypair', 'passwd']),
              help='指定登录方式。当为 linux 主机时，有效值为 keypair 和 passwd; '
                   '当为 windows 主机时，只能选用 passwd 登录方式。'
                   '当登录方式为 keypair 时，需要指定 login_keypair 参数；'
                   '当登录方式为 passwd 时，需要指定 login_passwd 参数。')
@click.option('-login_keypair', type=str,
              help='登录密钥ID')
@click.option('-login_passwd', type=str,
              help='登录密码')
@click.option('-security_group', type=str,
              help='主机加载的防火墙ID，只有在 vxnets.n 包含基础网络（即：vxnet-0）时才需要提供。'
                   ' 若未提供，则默认加载缺省防火墙')
@click.option('-volumes', type=str,
              help='主机创建后自动加载的硬盘ID，如果传此参数，则参数 count 必须为1')
@click.option('-hostname', type=str,
              help='可指定主机的 hostname')
@click.option('-need_newsid', type=click.Choice(['0', '1']),
              help='1: 生成新的SID，0: 不生成新的SID, 默认为0；只对Windows类型主机有效')
@click.option('-instance_class', type=click.Choice(['0', '1', '101', '201']),
              help='主机性能类型: 性能型:0, 超高性能型:1, 基础型:101, 企业型:201')
@click.option('-cpu_model', type=click.Choice(['Westmere', 'SandyBridge', 'IvyBridge', 'Haswell', 'Broadwell']),
              help='CPU 指令集, 有效值: Westmere, SandyBridge, IvyBridge, Haswell, Broadwell')
@click.option('-cpu_topology', type=click.Choice(['0', '1']),
              help='CPU 拓扑结构: 插槽数, 核心数, 线程数; 插槽数 * 核心数 * 线程数 应等于您应选择的CPU数量。')
@click.option('-gpu', type=str,
              help='GPU 个数')
@click.option('-gpu_class', type=click.Choice(['0', '1']),
              help='GPU 类型，有效值有 0 和 1 。0 对应的是 NVIDIA P100，1 对应的是 AMD S7150')
@click.option('-nic_mqueue', type=click.Choice(['0', '1']), default="0",
              help='网卡多对列: 关闭(默认)：0，开启：1')
@click.option('-need_userdata', type=click.Choice(['0', '1']), default="0",
              help='1: 使用 User Data 功能；0: 不使用 User Data 功能；默认为 0 ')
@click.option('-userdata_type', type=click.Choice(['plain', 'exec']),
              help='User Data 类型，有效值：’plain’, ‘exec’ 或 ‘tar’。'
                   '为 ‘plain’或’exec’ 时，使用一个 Base64 编码后的字符串；'
                   '为 ‘tar’ 时，使用一个压缩包（种类为 zip，tar，tgz，tbz）')
@click.option('-userdata_value', type=str,
              help='User Data 值。'
                   '当类型为 ‘plain’ 时，为字符串的 Base64 编码值，长度限制 4K；'
                   '当类型为 ‘tar’，为调用 UploadUserDataAttachment 返回的 attachment_id。')
@click.option('-userdata_path', type=str,
              help='User Data 和 MetaData 生成文件的存放路径。不输入或输入不合法时，为默认目录 /etc/qingcloud/userdata')
@click.option('-userdata_file', type=str,
              help='userdata_type 为 ‘exec’ 时，指定生成可执行文件的路径，默认为/etc/rc.local')
@click.option('-target_user', type=str,
              help='目标用户 ID ，可用于主账号为其子账号创建资源')
@click.option('-dedicated_host_group_id', type=str,
              help='虚机创建到指定的专属宿主机组中')
@click.option('-dedicated_host_id', type=str,
              help='虚机创建到某专属宿主机组中指定的宿主机上')
@click.option('-instance_group', type=str,
              help='虚机创建加入到指定的主机组中')
@click.option('-hypervisor', type=click.Choice(['kvm', 'bm']), default='kvm',
              help='hypervisor 类型，当前支持 kvm 和 bm, 默认是 kvm')
@click.option('-os_disk_encryption', type=click.Choice(['true', 'false']),
              help='创建加密主机')
@click.option('-cipher_alg', type=str, default='aes256',
              help='加密使用的算法类型: 目前仅支持 aes256，默认 aes256')
@click.option('-months', type=str,
              help='如果购买合约模式的主机，需要传此参数，数值为购买的月份数。')
@click.option('-auto_renew', type=str,
              help='如果购买合约模式的主机，可传此参数，数值为合约到期后自动续约的月份数。'
                   '如果购买合约时不传此参数，合约到期则不会自动续约')
@click.option('-zone', prompt='区域 ID：', type=str,
              help='主机所在的的区域ID')
def run_instances(zone, count, *args, **kwargs):
    """
    创建指定配置，指定数量的主机。
    当你创建主机时，主机会先进入 pending 状态，直到创建完成后，变为 running 状态。
    你可以使用 DescribeInstances 检查主机状态。
    创建主机时，一旦参数 vxnets.n 包含基础网络（即： vxnet-0 ），则需要指定防火墙 security_group，
    如果没有指定，青云会自动使用缺省防火墙。
    青云给主机定义了几种经典配置，可通过参数 instance_type 指定，配置列表请参考 Instance Types。
    如果经典配置不能满足你的需求，可通过参数 cpu, memory 自定义主机配置。
    如果参数中既指定 instance_type ，又指定了 cpu 和 memory ， 则以指定的 cpu 和 memory 为准。
    """
    click.echo(f"在当前区域id[{zone}]下的创建{count}台主机，状态为running")


if __name__ == '__main__':
    run_instances()
