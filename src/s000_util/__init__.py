try:
    from s000_util import s000_get_config as sgc
    n = sgc.aws_access()
    print(n.aws_accesskey)

except Exception as e:
    print("problem {}".format(e))