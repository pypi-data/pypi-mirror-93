import click
import psutil


@click.command()
@click.option("-c", "--cpu", default=False, is_flag=True)
@click.option("-m", "--memroy", default=False, is_flag=True)
@click.option("-d", "--disk", default=False, is_flag=True)
def cli(cpu, memroy, disk):
    if cpu:
        res = "{:.2f}".format(psutil.cpu_freq().current / 1000) + " GHz "
        res += f"{psutil.cpu_count(logical=False)}核"
        res += f" {psutil.cpu_count()}线程"
        print(res)
        return
    if memroy:
        mem = psutil.virtual_memory()
        total = "{:.2f}".format(mem.total / 1073741824)
        available = "{:.2f}".format(mem.available / 1073741824)
        print(f"total: {total}G\navailable: {available}G")
        return
    if disk:
        usage = psutil.disk_usage("/")
        total = "{:.2f}".format(usage.total / (10 ** 9))
        free = "{:.2f}".format(usage.free / (10 ** 9))
        print(f"total: {total}G\nfree: {free}G")
        return
