VSISH_VSWITCH_PATH=/net/portsets
for vSwitch in $(vsish -e ls ${VSISH_VSWITCH_PATH});
do
   VSWITCH=$(echo ${vSwitch} | sed 's/\///g')
   for port in $(vsish -e ls ${VSISH_VSWITCH_PATH}/${vSwitch}ports);
   do
      PORT=$(echo ${port} | sed 's/\///g')
      PORTINFO=$(vsish -e get ${VSISH_VSWITCH_PATH}/${vSwitch}ports/${port}status | sed 's/^[ \t]*//;s/[ \t]*$//');
      CLIENT=$(echo ${PORTINFO} | sed 's/ /\n/g' | grep "clientName:" | awk -F ":" '{print $2}')
      MACADDRESS=$(echo ${PORTINFO} | sed 's/ /\n/g' | grep "unicastAddr:" | uniq | sed 's/unicastAddr://;s/\(.*\)./\1/')
      vmnics=$(echo -e "${PORT}\t${CLIENT}" | grep vmnic | awk '{ print $1 }')
      for i in $vmnics;
      do
         vsish -e typels /net/portsets/vSwitch0/ports/$i/lldp/enable
         vsish -e set /net/portsets/vSwitch0/ports/$i/lldp/enable 1
      done
   done
done
