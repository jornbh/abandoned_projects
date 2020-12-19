#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "nrf.h"
#include "ble_master.h"


/*The BLE-packet being transmitted*/
static uint8_t ble_adv_data_master[10] = {0x00,0x06,0x00,0x9A,0x78,0x56,0x34,0x12,0xaa,0xff};

void radio_setup_master(void) 
{
	gpio_setup_master();
	gpiote_setup_master();
	ppi_setup_master();
	timer_setup_master();
	
	NRF_RADIO->PACKETPTR = (uint32_t) &(ble_adv_data_master[0]);
}


void gpiote_setup_master(void)
{
	/* GPIOTE setup for master.
	OUT[0] = BUTTON1->PIN1 - Master Clock
	IN[1] = BUTTON1->START - Trigger RADIO start
	OUT[2] = ADDRESS_END->PIN2 Debug
	OUT[3] = END->LED2 visuals
	*/
	
	NRF_GPIOTE->CONFIG[0] = ((GPIOTE_CONFIG_MODE_Task << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk)
													|	((1UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)
													| ((GPIOTE_CONFIG_POLARITY_Toggle << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk)
													| ((GPIOTE_CONFIG_OUTINIT_Low << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);

	NRF_GPIOTE->CONFIG[1] = ((GPIOTE_CONFIG_MODE_Event << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk)
													|	((17UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)
													| ((GPIOTE_CONFIG_POLARITY_HiToLo << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk)
													| ((GPIOTE_CONFIG_OUTINIT_High << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);
		
	NRF_GPIOTE->CONFIG[2] = ((GPIOTE_CONFIG_MODE_Task << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk)
													|	((2UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)
													| ((GPIOTE_CONFIG_POLARITY_Toggle << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk)
													| ((GPIOTE_CONFIG_OUTINIT_Low << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);
		
	NRF_GPIOTE->CONFIG[3] =  ((GPIOTE_CONFIG_MODE_Task << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk) 
													| ((22UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)
													| ((GPIOTE_CONFIG_POLARITY_Toggle << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk)
													| ((GPIOTE_CONFIG_OUTINIT_High << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);
}


void ppi_setup_master(void)
{
	
	/* Setup PPI-channels for master
	0. BUTTON1 Pressed -> RADIO_START
	1. BUTTON1 Pressed -> Master Clock High
	2. RADIO_END ->  Toggle LED2
	3. RADIO_END -> Toggle Pin2
	*/
	
	NRF_PPI->CHENSET |= ((PPI_CHENSET_CH0_Enabled << PPI_CHENSET_CH0_Pos) & PPI_CHENSET_CH0_Msk)
											| ((PPI_CHENSET_CH1_Enabled << PPI_CHENSET_CH1_Pos) & PPI_CHENSET_CH1_Msk)
											| ((PPI_CHENSET_CH2_Enabled << PPI_CHENSET_CH2_Pos) & PPI_CHENSET_CH2_Msk)
											| ((PPI_CHENSET_CH3_Enabled << PPI_CHENSET_CH3_Pos) & PPI_CHENSET_CH3_Msk);

		NRF_PPI->CH[0].EEP = (uint32_t) &(NRF_GPIOTE->EVENTS_IN[1]);
		NRF_PPI->CH[0].TEP = (uint32_t) &(NRF_RADIO->TASKS_START);
		
		NRF_PPI->CH[1].EEP = (uint32_t) &(NRF_GPIOTE->EVENTS_IN[1]);
		NRF_PPI->CH[1].TEP = (uint32_t) &(NRF_GPIOTE->TASKS_OUT[0]);
	
		NRF_PPI->CH[2].EEP = (uint32_t) &(NRF_RADIO->EVENTS_END);
		NRF_PPI->CH[2].TEP = (uint32_t) &(NRF_GPIOTE->TASKS_OUT[2]);
		
		NRF_PPI->CH[3].EEP = (uint32_t) &(NRF_RADIO->EVENTS_END);
		NRF_PPI->CH[3].TEP = (uint32_t) &(NRF_GPIOTE->TASKS_OUT[3]);
		
}


void timer_setup_master(void) 
{
	/* Timer module for master. Not needed so far */
}


void gpio_setup_master(void)
{
	/* We will enable all the remaining LEDs as outputs for debugging aswell as enable Pull-Up on Button 1*/
	NRF_GPIO->PIN_CNF[21] = ((GPIO_PIN_CNF_DIR_Output << GPIO_PIN_CNF_DIR_Pos) & GPIO_PIN_CNF_DIR_Msk)
												| ((GPIO_PIN_CNF_DRIVE_S0S1 << GPIO_PIN_CNF_DRIVE_Pos) & GPIO_PIN_CNF_DRIVE_Msk);
	NRF_GPIO->PIN_CNF[23] = ((GPIO_PIN_CNF_DIR_Output << GPIO_PIN_CNF_DIR_Pos) & GPIO_PIN_CNF_DIR_Msk)
												| ((GPIO_PIN_CNF_DRIVE_S0S1 << GPIO_PIN_CNF_DRIVE_Pos) & GPIO_PIN_CNF_DRIVE_Msk);
	NRF_GPIO->PIN_CNF[24] = ((GPIO_PIN_CNF_DIR_Output << GPIO_PIN_CNF_DIR_Pos) & GPIO_PIN_CNF_DIR_Msk)
												| ((GPIO_PIN_CNF_DRIVE_S0S1 << GPIO_PIN_CNF_DRIVE_Pos) & GPIO_PIN_CNF_DRIVE_Msk);
	
	NRF_GPIO->PIN_CNF[17] = ((GPIO_PIN_CNF_DIR_Input << GPIO_PIN_CNF_DIR_Pos) & GPIO_PIN_CNF_DIR_Msk)
												|	((GPIO_PIN_CNF_PULL_Pullup << GPIO_PIN_CNF_PULL_Pos) & GPIO_PIN_CNF_PULL_Msk)
												|	((GPIO_PIN_CNF_SENSE_Low << GPIO_PIN_CNF_SENSE_Pos) & GPIO_PIN_CNF_SENSE_Msk);
	

	/* Initialize the LEDs to off (high*/
	NRF_GPIO->OUT |= 	((GPIO_OUT_PIN21_High << GPIO_OUT_PIN21_Pos) & GPIO_OUT_PIN21_Msk)
								|	 	((GPIO_OUT_PIN23_High << GPIO_OUT_PIN23_Pos) & GPIO_OUT_PIN23_Msk)
								|		((GPIO_OUT_PIN24_High << GPIO_OUT_PIN24_Pos) & GPIO_OUT_PIN24_Msk);
}
