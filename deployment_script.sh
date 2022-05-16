#!/usr/bin/env bash
set -e

echo "===== Untar infrastructure-plant tar gz ===="
cd infrastructure-plant/infrastructure-plant
sudo tar  -xzvf infrastructure-plant.tar.gz .
sudo rm -f infrastructure-plant.tar.gz
echo "====== Untar Configuration-plant.tar.gz ====="
cd ../../aivi-fcm-ac-configuration/configuration-plant
sudo tar xzvf configuration-plant.tar.gz .
sudo rm -f configuration-plant.tar.gz

echo "************ Setup Central Station ***********"
cd ../../infrastructure-plant/infrastructure-plant
sudo touch .vault_pass.txt
echo $VAULT_PASSWORD >> .vault_pass.txt
echo $IP_ADDRESS
echo $STATION_NAME


ansible-playbook AIVI-system.yml  --vault-password-file .vault_pass.txt  -e "stations=[{\"ip\":\"$IP_ADDRESS\",\"station_name\":\"$STATION_NAME\"}] sas_token=$DEVOPS_ARTIFACT_SAS_TOKEN
HTTPS_PROXY=$HTTPS_PROXY HTTP_PROXY=$HTTP_PROXY ansible_roles=$ANSIBLE_ROLES" --skip-tags "spacewalk, nvidia_kernel_update, hydra_agent, cybereason_antivirus"

echo "=========================Download fake images======================================="
mkdir -p $ANSIBLE_ROLES/fake_images/files/



echo "==== Download fake images from Blob-Strorage ===="

cd $AZCOPY_DIRECTORY

	   ./azcopy copy "https://staivifcmmldev.blob.core.windows.net/model-evaluation/qualif/$FAKE_IMAGES/*$FCM_FAKE_SAS_TOKEN" $ANSIBLE_ROLES/fake_images/files/ --recursive=true


echo "=== Move configurations to Ansible roles ==="


mkdir -p $ANSIBLE_ROLES/configuration_files/files/
cd $WORK/aivi-fcm-ac-configuration/configuration-plant
cp -r $PLANT_NAME $ANSIBLE_ROLES/configuration_files/files/

echo "******** CONFIGURATION FILES TO BE DEPLOYED *******"
ls -l $ANSIBLE_ROLES/configuration_files/files/
ls -l $ANSIBLE_ROLES/configuration_files/files/$PLANT_NAME/
ls -l $ANSIBLE_ROLES/configuration_files/files/$PLANT_NAME/$STATION_NAME/

echo  "===== Move models to Ansible roles ==="
mkdir -p $ANSIBLE_ROLES/deploy_models/files/models/

cd $WORK/aivi-fcm-ac-ci-cd/fcm-assemblycheck-RMP-ES1
cp -r  .  $ANSIBLE_ROLES/deploy_models/files/models/

echo "******** NEW MODEL FILES TO BE DEPLOYED *******"
ls $ANSIBLE_ROLES/deploy_models/files/models/

echo "==== Move fcm-assemblycheck codebase to Ansible roles ===="
cd $WORK/aivi-fcm-ac-ci-cd/fcm-assemblycheck
ls .

mkdir -p $ANSIBLE_ROLES/deploy_codebase/files/

cp fcm-assemblycheck-*.tar.gz $ANSIBLE_ROLES/deploy_codebase/files/

echo "******** CODEBASE TO BE DEPLOYED *******"
ls $ANSIBLE_ROLES/deploy_codebase/files/

echo  "=== Set value for APP_VERSION ==="
export APP_VERSION=$(ls $ANSIBLE_ROLES/deploy_codebase/files/f*-*.tar.gz | grep -Po '\d.\d*.\d.*(?=.tar.gz)')
echo APP_VERSION: $APP_VERSION
echo "##vso[task.setvariable variable=APP_VERSION]$APP_VERSION"

echo "******* Deployement on the Edge Station"
cd $WORK/infrastructure-plant/infrastructure-plant

ansible-playbook FCM-AssemblyCheck.yml --vault-password-file .vault_pass.txt -e "app_name=fcm-assemblycheck app_version=$APP_VERSION plant_name=$PLANT_NAME stations=[{\"ip\":\"$IP_ADDRESS\",\"station_name\":\"$STATION_NAME\"}] sas_token=$DEVOPS_ARTIFACT_SAS_TOKEN ansible_roles=$ANSIBLE_ROLES
HTTPS_PROXY=$HTTPS_PROXY HTTP_PROXY=$HTTP_PROXY"
