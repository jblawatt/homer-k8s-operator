
import kopf
import yaml
from kubernetes import config as k_config, client as k_client


class HomerServiceDefinition:

    singular = "homerservice"
    plural = "homerservices"
    version = "v1"
    group = "homer-operator.j3nko.de"


hsdef = HomerServiceDefinition()


class HomerConfigDefinition:

    singular = "homerconfig"
    plural = "homerconfig"
    version = "v1"
    group = "homer-operator.j3nko.de"


hcdef = HomerConfigDefinition()

required = True
not_required = False


query = (
    ("group", required),
    ("name", required),
    ("logo", not_required),
    ("subtitle", not_required),
    ("tag", not_required),
    ("keyword", not_required),
    ("target", not_required),
    ("tagstyle", not_required),
)


def extract_homerconfigmap_filter():
    api = k_client.CoreV1Api()

    homer_configs = kapi.list_cluster_custom_object(
        group=hcdef.group,
        version=hcdef.version,
        plural=hcdef.plural,
    )
    
    if homer_configs:
        # api_version = homer_configs.get("apiVersion")  # type: ignore
        for item in homer_configs.get("items"):
            # spec contains relevant filter
            # - group
            # - name
            # - namespace
            return item.get("spec")

        raise RuntimeError("no configuration found")



@kopf.on.create("networking.k8s.io", "v1", "Ingress")
def on_ingress_create(body, *args, **kwargs):

    meta = body["metadata"]
    annotations = meta.get("annotations", {})

    match annotations:
        case {"homer-operator.j3nko.de/servicename": service_name,
              "homer-operator.j3nko.de/group": group_name}:
            print("got new service name", service_name)

            # https://notebook.community/mbohlool/client-python/examples/notebooks/create_configmap
            k_config.load_kube_config()

            configmap_filter = extract_homerconfigmap_filter()

            api = k_client.CoreV1Api()
            configmap_query = api.list_namespaced_config_map( **configmap_filter)


            for item in configmap_query.get("items"):
                yaml_spec = item["data"]["homer.yaml"]
                spec = yaml.load(yaml_spec, Loader=yaml.FullLoader)

                service_obj = {}
                for key in query:
                    if key == "group":
                        pass
                    if value := annotations.get(f"homer-operator.j3nko.de/{key}"):
                        service_obj[key] = value


            #if homer_configs:
            #    # api_version = homer_configs.get("apiVersion")  # type: ignore
            #    for item in homer_configs.get("items"):
            #        name = item["metadata"]["name"]
            #        namespace = item["metadata"]["namespace"]
            #        services = set(item.get("spec", {}).get("services", ()))
            #        services.add(service_name)
            #        print(f"patching {name} with {services}")
            #        kapi.patch_namespaced_custom_object(
            #            group=hcdef.group,
            #            plural=hcdef.plural,
            #            version=hcdef.version,
            #            name=name,
            #            namespace=namespace,
            #            body={"spec": {"services": list(services)}},
            #        )

        case _:
            print("not a relevant ingress")

