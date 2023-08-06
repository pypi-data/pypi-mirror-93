#!/bin/bash
#
#
# Copyright 2013 AppDynamics.
# All rights reserved.
#
#

## Lines that begin with ## will be stripped from this file as part of the
## agent build process.

# BASE_DIR refers to the directory containing the runProxy
BASE_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

runProxyScript=${BASE_DIR}/runProxy
runProxyScriptDir=${BASE_DIR}

jreDir=
# If JAVA_HOME is set, jreDir gets picked up from there
if [ -n "${JAVA_HOME}" ] ; then
    jreDir="${JAVA_HOME}"
fi

verbose=

usage() {

cat << EOF
Usage: `basename $0`
Options:
  -j <dir>, --jre-dir=<dir>             Specifies root JRE directory
  -v, --verbose                         Enable verbose output
  -h,--help                             Show this message

Example: $0 -j /usr
Note: Please use quotes for the entries wherever applicable.

EOF
}

optspec=":j:vh-:"
while getopts "$optspec" optchar; do
    case "${optchar}" in
        -)
            case "${OPTARG}" in
                help)
                    usage
                    exit 1
                    ;;
                jre-dir=*)
                    jreDir=${OPTARG#*=}
                    ;;
                verbose)
                    verbose=yes
                    ;;
                *)
                    echo "Invalid option: '--${OPTARG}'" >&2
                    ok=0
                    ;;
            esac;;
        j)
            jreDir=${OPTARG#*=}
            ;;
        v)
            verbose=yes
            ;;
        h)
            usage
            exit 1
            ;;
        *)
            if [ "$OPTERR" != 1 ] || [ "${optspec:0:1}" = ":" ]; then
                echo "Invalid option: '-${OPTARG}'" >&2
                ok=0
            fi
            ;;
    esac
done

# If environment variable not set, default to /tmp/appd
agentBaseDir=/tmp/appd
if [ "${APPDYNAMICS_AGENT_BASE_DIR}" ] ; then
    agentBaseDir=${APPDYNAMICS_AGENT_BASE_DIR}
fi

# If environment variable not set, default to ${agentBaseDir}/run
proxyRunDir=
if [ -z "${APPDYNAMICS_PROXY_RUN_DIR}" ] ; then
    proxyRunDir=${agentBaseDir}/run
else
    proxyRunDir=${APPDYNAMICS_PROXY_RUN_DIR}
fi

# If environment variable not set, default to ${proxyRunDir}/comm
commDir=
if [ -z "${APPDYNAMICS_PROXY_CONTROL_PATH}" ] ; then
    commDir=${proxyRunDir}/comm
else
    commDir=${APPDYNAMICS_PROXY_CONTROL_PATH}
fi

# If environment variable not set, default to ${agentBaseDir}/logs
logsDir=
if [ -z "${APPDYNAMICS_LOGS_DIR}" ] ; then
    logsDir=${agentBaseDir}/logs
else
    logsDir=${APPDYNAMICS_LOGS_DIR}
fi

mkdir -p -m 777 "$proxyRunDir"
mkdir -p -m 777 "$commDir"
mkdir -p -m 777 "$logsDir"

runCmd=()
runCmd[${#runCmd[@]}]="${runProxyScript}"
if [ -n "${jreDir}" ] ; then
    runCmd[${#runCmd[@]}]="--jre-dir=${jreDir}"
fi
runCmd[${#runCmd[@]}]="--proxy-dir=${runProxyScriptDir}"
runCmd[${#runCmd[@]}]="--proxy-runtime-dir=${proxyRunDir}"
if [ -n "${verbose}" ]  ; then
    runCmd[${#runCmd[@]}]="-v"
fi

# Append these variables only if the corresponding environment variable exists
if [ -n "${APPDYNAMICS_MAX_HEAP_SIZE}" ] ; then
    runCmd[${#runCmd[@]}]="--max-heap-size=${APPDYNAMICS_MAX_HEAP_SIZE}"
fi
if [ -n "${APPDYNAMICS_MIN_HEAP_SIZE}" ] ; then
    runCmd[${#runCmd[@]}]="--min-heap-size=${APPDYNAMICS_MIN_HEAP_SIZE}"
fi
if [ -n "${APPDYNAMICS_MAX_PERM_SIZE}" ] ; then
    runCmd[${#runCmd[@]}]="--max-perm-size=${APPDYNAMICS_MAX_PERM_SIZE}"
fi
if [ -n "${APPDYNAMICS_HTTP_PROXY_HOST}" ] ; then
    runCmd[${#runCmd[@]}]="--http-proxy-host=${APPDYNAMICS_HTTP_PROXY_HOST}"
fi
if [ -n "${APPDYNAMICS_HTTP_PROXY_PORT}" ] ; then
    runCmd[${#runCmd[@]}]="--http-proxy-port=${APPDYNAMICS_HTTP_PROXY_PORT}"
fi
if [ -n "${APPDYNAMICS_HTTP_PROXY_USER}" ] ; then
    runCmd[${#runCmd[@]}]="--http-proxy-user=${APPDYNAMICS_HTTP_PROXY_USER}"
fi
if [ -n "${APPDYNAMICS_HTTP_PROXY_PASSWORD_FILE}" ] ; then
    runCmd[${#runCmd[@]}]="--http-proxy-password-file=${APPDYNAMICS_HTTP_PROXY_PASSWORD_FILE}"
fi
if [ -n "${APPDYNAMICS_START_SUSPENDED}" ] ; then
    runCmd[${#runCmd[@]}]="--start-suspended=${APPDYNAMICS_START_SUSPENDED}"
fi
if [ -n "${APPDYNAMICS_PROXY_DEBUG_PORT}" ] ; then
    runCmd[${#runCmd[@]}]="--proxy-debug-port=${APPDYNAMICS_PROXY_DEBUG_PORT}"
fi
if [ -n "${APPDYNAMICS_DEBUG_OPT}" ] ; then
    runCmd[${#runCmd[@]}]="--debug-opt=${APPDYNAMICS_DEBUG_OPT}"
fi
if [ -n "${APPDYNAMICS_AGENT_TYPE}" ] ; then
    runCmd[${#runCmd[@]}]="--agent-type=${APPDYNAMICS_AGENT_TYPE}"
fi

runCmd[${#runCmd[@]}]="${commDir}"
runCmd[${#runCmd[@]}]="${logsDir}"

if [ -n "${APPDYNAMICS_AGENT_UNIQUE_HOST_ID}" ] ; then
    runCmd[${#runCmd[@]}]="-Dappdynamics.agent.uniqueHostId=${APPDYNAMICS_AGENT_UNIQUE_HOST_ID}"
fi
if [ -n "${APPDYNAMICS_TCP_COMM_PORT}" ] ; then
    runCmd[${#runCmd[@]}]="-Dcommtcp=${APPDYNAMICS_TCP_COMM_PORT}"
    if [ -n "${APPDYNAMICS_TCP_COMM_HOST}" ] ; then
        runCmd[${#runCmd[@]}]="-Dappdynamics.proxy.commtcphost=${APPDYNAMICS_TCP_COMM_HOST}"
    fi
    if [ -n "${APPDYNAMICS_TCP_PORT_RANGE}" ] ; then
        runCmd[${#runCmd[@]}]="-Dappdynamics.proxy.commportrange=${APPDYNAMICS_TCP_PORT_RANGE}"
    fi
fi

if [ -n "${verbose}" ]  ; then
    echo ${runCmd[@]}
fi

umask 011
exec "${runCmd[@]}"