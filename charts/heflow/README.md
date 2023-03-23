# HEflow

A Privacy-Preserving Machine Learning Lifecycle Platform

## Installing the Chart

To install the chart with the release name `my-heflow`:

```console
$ helm install my-heflow .
```

These commands deploy HEflow on the Kubernetes cluster in the default
configuration.

> **Tip**: List all releases using `helm list`

## Uninstalling the Chart

To uninstall/delete the `my-heflow` deployment:

```console
$ helm uninstall my-heflow
```

The command removes all the Kubernetes components associated with the chart and
deletes the release.

## Parameters

The following table lists the configurable parameters of the HEflow chart and
their default values.

| Parameter           | Description                                   | Default          |
| ------------------- | --------------------------------------------- | ---------------- |
| `heflow.image`      | Container image name.                         | `inaccel/heflow` |
| `heflow.pullPolicy` | Image pull policy.                            |                  |
| `heflow.resources`  | Compute resources required by this container. |                  |
| `heflow.tag`        | Release version.                              | `latest`         |
| `replicas`          | Number of desired pods.                       |                  |

Specify each parameter using the `--set key=value[,key=value]` argument to
`helm install`.

Alternatively, a YAML file that specifies the values for the parameters can be
provided while installing the chart. For example,

```console
$ helm install my-heflow -f values.yaml inaccel/heflow
```

> **Tip**: You can use the default `values.yaml`
