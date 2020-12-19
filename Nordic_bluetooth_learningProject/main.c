#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "nrf.h"
#include "ble_master.h"
#include "ble_slave.h"
#include "settings.h"
#include "pca10028/blank/arm5_no_packs/ble_common_setup.h"

/* radio_init will initialize the RADIO and ramp it up and leave it in TXIDLE. For the role-specific (master/slave) initialization we use 
the setup functions in ble_master.c and ble_slave.c */

void ble_radio_setup_p2p(); 


int main() 
{
	clock_initialization();
	radio_init();
	
	ble_radio_setup_p2p(); 
	while (1) {}


	}

	
