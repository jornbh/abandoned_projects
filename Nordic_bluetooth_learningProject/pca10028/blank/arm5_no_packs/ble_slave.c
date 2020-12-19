#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "nrf.h"
#include "ble_slave.h"

static uint8_t ble_adv_data_slave[10] = {0x00,0x06,0x00,0x9A,0x78,0x56,0x34,0x12,0xaf,0xff};


void radio_setup_slave(void)
{
	gpio_setup_slave();
	timer_setup_slave();
	gpiote_setup_slave();
	ppi_setup_slave();
	
	NRF_RADIO->PACKETPTR = (uint32_t) &(ble_adv_data_slave[0]);
} 


void timer_setup_slave(void)
{
	//TODO: Add a delay function parameter
	
	/*Setup Shorting */
	NRF_TIMER0->SHORTS = ((TIMER_SHORTS_COMPARE0_CLEAR_Enabled << TIMER_SHORTS_COMPARE0_CLEAR_Pos) & TIMER_SHORTS_COMPARE0_CLEAR_Msk)
											|((TIMER_SHORTS_COMPARE0_STOP_Enabled << TIMER_SHORTS_COMPARE0_STOP_Pos) & TIMER_SHORTS_COMPARE0_STOP_Msk);
	
	NRF_TIMER0->BITMODE = TIMER_BITMODE_BITMODE_32Bit;
	
	NRF_TIMER0->PRESCALER = 8; 
	NRF_TIMER0->CC[0] = 32;
}

void gpiote_setup_slave(void)
{
	/* GPIOTE setup for slave.
	IN[0] - Master Drive Signal (PIN1)
	OUT[1] - LED2 (on RADIO_END)
	OUT[2] - PIN2 (On RADIO_END)
	IN[3] - Button4 (Trigger RADIO_START)
	*/
	
	NRF_GPIOTE->CONFIG[0] = ((GPIOTE_CONFIG_MODE_Event << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk)
													|	((1UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)
													| ((GPIOTE_CONFIG_POLARITY_Toggle << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk)
													| ((GPIOTE_CONFIG_OUTINIT_Low << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);

	NRF_GPIOTE->CONFIG[1] = ((GPIOTE_CONFIG_MODE_Event << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk)
													|	((17UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)
													| ((GPIOTE_CONFIG_POLARITY_HiToLo << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk)
													| ((GPIOTE_CONFIG_OUTINIT_High << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);
		
	NRF_GPIOTE->CONFIG[2] = ((GPIOTE_CONFIG_MODE_Task << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk)
													|	((22UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)
													| ((GPIOTE_CONFIG_POLARITY_Toggle << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk)
													| ((GPIOTE_CONFIG_OUTINIT_Low << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);
													
	NRF_GPIOTE->CONFIG[3] = ((GPIOTE_CONFIG_MODE_Event << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk)
													|	((20UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)
													| ((GPIOTE_CONFIG_POLARITY_HiToLo << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk)
													| ((GPIOTE_CONFIG_OUTINIT_High << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);
													
}

void ppi_setup_slave(void) 
{
	/*
	CH0: Master Drive -> TIMER_START
	CH1: TIMER_CC -> RADIO_START
	CH2: RADIO_END -> TOGGLE_LED
	CH3: BUTTON4_PRESSED -> RADIO_START  For debug 
	*/
	
	NRF_PPI->CHENSET |=   ((PPI_CHENSET_CH0_Enabled << PPI_CHENSET_CH0_Pos) & PPI_CHENSET_CH0_Msk)
											| ((PPI_CHENSET_CH1_Enabled << PPI_CHENSET_CH1_Pos) & PPI_CHENSET_CH1_Msk)
											| ((PPI_CHENSET_CH2_Enabled << PPI_CHENSET_CH2_Pos) & PPI_CHENSET_CH2_Msk)
											| ((PPI_CHENSET_CH3_Enabled << PPI_CHENSET_CH3_Pos) & PPI_CHENSET_CH3_Msk);
	
		NRF_PPI->CH[0].EEP = (uint32_t) &(NRF_GPIOTE->EVENTS_IN[0]);
		NRF_PPI->CH[0].TEP = (uint32_t) &(NRF_TIMER0->TASKS_START);
		
		NRF_PPI->CH[1].EEP = (uint32_t) &(NRF_TIMER0->EVENTS_COMPARE);
		NRF_PPI->CH[1].TEP = (uint32_t) &(NRF_RADIO->TASKS_START);
	
		NRF_PPI->CH[2].EEP = (uint32_t) &(NRF_RADIO->EVENTS_END);
		NRF_PPI->CH[2].TEP = (uint32_t) &(NRF_GPIOTE->TASKS_OUT[2]);
	
		NRF_PPI->CH[3].EEP = (uint32_t) &(NRF_GPIOTE->EVENTS_IN[3]);
		NRF_PPI->CH[3].TEP = (uint32_t) &(NRF_RADIO->TASKS_START);
}
	

void gpio_setup_slave(void)
{
		NRF_GPIO->PIN_CNF[20] = ((GPIO_PIN_CNF_DIR_Input << GPIO_PIN_CNF_DIR_Pos) & GPIO_PIN_CNF_DIR_Msk)
												|	((GPIO_PIN_CNF_PULL_Pullup << GPIO_PIN_CNF_PULL_Pos) & GPIO_PIN_CNF_PULL_Msk)
												|	((GPIO_PIN_CNF_SENSE_Low << GPIO_PIN_CNF_SENSE_Pos) & GPIO_PIN_CNF_SENSE_Msk);
}













