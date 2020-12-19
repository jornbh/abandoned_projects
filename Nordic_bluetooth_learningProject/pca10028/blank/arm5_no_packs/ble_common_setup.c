#include <stdint.h>
#include "nrf.h"


#include "settings.h"

void radio_init(void)
{
	/* Turn radio on and off to reset all registers */
	NRF_RADIO->POWER = RADIO_POWER_POWER_Disabled << RADIO_POWER_POWER_Pos;
  	NRF_RADIO->POWER = RADIO_POWER_POWER_Enabled << RADIO_POWER_POWER_Pos;
	
	NRF_RADIO->EVENTS_DISABLED = 0;
	
	/* Set radio configuration paramteres*/
	NRF_RADIO->TXPOWER = (RADIO_TXPOWER_TXPOWER_0dBm << RADIO_TXPOWER_TXPOWER_Pos); //0dBm
	NRF_RADIO->MODE = (RADIO_MODE_MODE_Ble_1Mbit << RADIO_MODE_MODE_Pos);//BLE_1Mbit
	

	NRF_RADIO->FREQUENCY = BLE_FREQUENCY; //Channel 37,38 or 39 (Specified in settings.h)
	NRF_RADIO->DATAWHITEIV = BLE_CHANNEL; //Correseponds to frequency

	
	
	/* Configure Access Address to be the BLE standard */
	NRF_RADIO->BASE0 = 0x89bed600;
	NRF_RADIO->PREFIX0 = 0x8e;

	NRF_RADIO->TXADDRESS = 0x00;
	NRF_RADIO->RXADDRESSES = 0x00; //Enable reception on logical address 0

	/* Configure the length of the S0, S1 and length field to match a advertisement package*/
	NRF_RADIO->PCNF0 = (
			(((1UL) << RADIO_PCNF0_S0LEN_Pos) & RADIO_PCNF0_S0LEN_Msk)
		|	(((2UL) << RADIO_PCNF0_S1LEN_Pos) & RADIO_PCNF0_S1LEN_Msk)
		| (((6UL) << RADIO_PCNF0_LFLEN_Pos) & RADIO_PCNF0_LFLEN_Msk)
	);

/* Configure MAXLEN, STATLEN, BALEN, ENDIAN and WHITEEN */
	NRF_RADIO->PCNF1 = (
			(((37UL) << RADIO_PCNF1_MAXLEN_Pos) & RADIO_PCNF1_MAXLEN_Msk)
		| (((0UL) << RADIO_PCNF1_STATLEN_Pos) & RADIO_PCNF1_STATLEN_Msk)
		| (((3UL) << RADIO_PCNF1_BALEN_Pos) & RADIO_PCNF1_BALEN_Msk)
		| ((RADIO_PCNF1_ENDIAN_Little << RADIO_PCNF1_ENDIAN_Pos) & RADIO_PCNF1_ENDIAN_Msk)
		| (((1UL) << RADIO_PCNF1_WHITEEN_Pos) & RADIO_PCNF1_WHITEEN_Msk)
	);
	
	/* CRC Config */
	NRF_RADIO->CRCCNF = (RADIO_CRCCNF_LEN_Three << RADIO_CRCCNF_LEN_Pos)
										|	(RADIO_CRCCNF_SKIPADDR_Skip << RADIO_CRCCNF_SKIPADDR_Pos);
	NRF_RADIO->CRCINIT = 0x555555;
	NRF_RADIO->CRCPOLY = 0x00065B;
	
	/*Lock interframe spacing so that we dont start RX too soon */
	//NRF_RADIO->TIFS = 150; //150 us
		
	/* Ramp up radio */
	NRF_RADIO->TASKS_TXEN = 1;
	while (NRF_RADIO->STATE != RADIO_STATE_STATE_TxIdle) {}
	
}

	

void clock_initialization()
{
	//TODO: The CLOCK is with all probability the root of all evil in this universe
    /* Start 16 MHz crystal oscillator */
    NRF_CLOCK->EVENTS_HFCLKSTARTED = 0;
    NRF_CLOCK->TASKS_HFCLKSTART    = 1;

    /* Wait for the external oscillator to start up */
    while (NRF_CLOCK->EVENTS_HFCLKSTARTED == 0)
    {
        // Do nothing.
    }
		
	NRF_CLOCK->LFCLKSRC = (CLOCK_LFCLKSRC_SRC_Synth << CLOCK_LFCLKSRC_SRC_Pos); // Use synthesized clock source since HFCLK is always running.
    NRF_CLOCK->EVENTS_LFCLKSTARTED 	= 0;        // Reset started event
    NRF_CLOCK->TASKS_LFCLKSTART 		= 1;        // Start the Low Frequency Clock
    while (NRF_CLOCK->EVENTS_LFCLKSTARTED == 0)   // Wait for it to be started
      {
      }
}

	
	void radio_shutdown(void)
	{
		NRF_RADIO->TASKS_STOP;
		NRF_RADIO->TASKS_DISABLE;
		
		NRF_TIMER1->TASKS_SHUTDOWN;
		NRF_TIMER1->POWER = 0;
		NRF_RADIO->POWER = 0;
	}



