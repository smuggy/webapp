GCP Setup necessary:
  gcloud container clusters get-credentials standard-cluster-1 --zone us-central1-a --project qs-todolist-232620


The commands to setup helm within the cluster:
  curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
  kubectl --namespace kube-system create sa tiller
  kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
  helm init --service-account tiller
  helm repo update
  kubectl get deploy,svc tiller-deploy -n kube-system


To install a helm chart:

  ## upload helm chart...
  helm install webapp-0.1.0.tgz


Create a service for Redis
kind: Service
apiVersion: v1
metadata:
  name: redis
spec:
  type: ClusterIP
  ports:
  - port: 6379
    targetPort: 6379

kind: Endpoints
apiVersion: v1
metadata:
  name: redis
subsets:
  - addresses:
      - ip: 10.128.0.8  ## corresponds to external (to cluster) ip
    ports:
      - port: 6379


http://localhost:8080/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login
