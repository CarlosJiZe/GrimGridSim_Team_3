class EnergyManagementSystem:
    """
    Manages energy distribution according to different priority strategies.
    
    This is the "brain" of the system that decides:
    - Where does solar energy go?
    - Where does deficit energy come from?
    """
    
    def __init__(self, strategy='LOAD_PRIORITY'):
        """
        Initialize the energy management system.
        
        Args:
            strategy (str): Priority strategy to use
                - 'LOAD_PRIORITY': House first, battery second, grid last
                - 'CHARGE_PRIORITY': Battery first, house second, grid last
                - 'PRODUCE_PRIORITY': Grid export first, battery second, house last
        """
        self._strategy = strategy

    def distribute_energy(self, solar_kw, load_kw, battery, grid, time_step_hours=1.0):
        """
        Distribute energy according to the selected strategy.
        
        Args:
            solar_kw (float): Available solar power in kW
            load_kw (float): House load demand in kW
            battery (Battery): Battery object
            grid (Grid): Grid object
            time_step_hours (float): Duration of time step in hours
            
        Returns:
            dict: Energy flows for logging
        """
        if self._strategy == 'LOAD_PRIORITY':
            return self._load_priority(solar_kw, load_kw, battery, grid, time_step_hours)
        
        elif self._strategy == 'CHARGE_PRIORITY':
            return self._charge_priority(solar_kw, load_kw, battery, grid, time_step_hours)
        
        elif self._strategy == 'PRODUCE_PRIORITY':
            return self._produce_priority(solar_kw, load_kw, battery, grid, time_step_hours)
        
        else:
            raise ValueError(f"Unknown strategy: {self._strategy}")

# ==============================LOAD_PRIORITY==========================================

    def _load_priority(self, solar_kw, load_kw, battery, grid, time_step_hours):
        """
        LOAD_PRIORITY: House first, battery second, grid export last.
        """
        # Initialize all energy flows
        solar_to_load = 0.0
        solar_to_battery = 0.0
        solar_to_grid = 0.0
        battery_to_load = 0.0
        grid_to_load = 0.0
        curtailed = 0.0
        
        solar_remaining = solar_kw

        # Step 1: Solar to House (Priority #1)
        if solar_remaining > 0:
            solar_to_load = min(solar_remaining, load_kw)
            solar_remaining -= solar_to_load
        
        # Step 2: Solar to Battery (Priority #2)
        # FIX: Check if battery is full BEFORE trying to charge
        if solar_remaining > 0 and not battery.is_full():
            offered_energy = solar_remaining * time_step_hours
            charged_energy = battery.charge(offered_energy)
            
            # Convert back to Power (kW)
            solar_to_battery = charged_energy / time_step_hours
            solar_remaining -= solar_to_battery
        
        # Step 3: Solar to Grid (Priority #3)
        if solar_remaining > 0:
            # Export limit is handled inside grid.export_energy
            exported_power = grid.export_energy(solar_remaining, time_step_hours)
            solar_to_grid = exported_power
            solar_remaining -= solar_to_grid
            
            # Any solar remaining here is effectively curtailed (Grid refused it)
            curtailed = solar_remaining

        # Step 4: Handle Deficit (Battery -> Grid)
        # Calculate what part of the load was NOT covered by solar
        deficit = load_kw - solar_to_load
        
        if deficit > 0:
            # 4a. Try Battery first
            requested_energy = deficit * time_step_hours
            discharged_energy = battery.discharge(requested_energy)
            battery_to_load = discharged_energy / time_step_hours
            deficit -= battery_to_load
            
            # 4b. Try Grid second
            if deficit > 0:
                grid.import_energy(deficit, time_step_hours)
                grid_to_load = deficit
        
        # Unmet load is whatever the grid couldn't provide (usually 0 unless grid fails)
        unmet_load = 0.0 # Assuming infinite grid availability for import
        
        return {
            'solar_to_load': round(solar_to_load, 6),
            'solar_to_battery': round(solar_to_battery, 6),
            'solar_to_grid': round(solar_to_grid, 6),
            'battery_to_load': round(battery_to_load, 6),
            'grid_to_load': round(grid_to_load, 6),
            'unmet_load': round(unmet_load, 6),
            'curtailed': round(curtailed, 6)
        }
        
# ==============================CHARGE_PRIORITY==========================================

    def _charge_priority(self, solar_kw, load_kw, battery, grid, time_step_hours):
        """
        CHARGE_PRIORITY: Battery first, house second, grid export last.
        """    
        # Initialize flows
        solar_to_load = 0.0
        solar_to_battery = 0.0
        solar_to_grid = 0.0
        battery_to_load = 0.0
        grid_to_load = 0.0
        curtailed = 0.0
        
        solar_remaining = solar_kw
        
        # Step 1: Solar to Battery (Priority #1)
        # FIX: Check if battery is full BEFORE trying to charge
        if solar_remaining > 0 and not battery.is_full():
            offered_energy = solar_remaining * time_step_hours
            charged_energy = battery.charge(offered_energy)
            
            solar_to_battery = charged_energy / time_step_hours
            solar_remaining -= solar_to_battery
            
        # Step 2: Solar to House (Priority #2)
        if solar_remaining > 0:
            solar_to_load = min(solar_remaining, load_kw)
            solar_remaining -= solar_to_load
                
        # Step 3: Solar to Grid (Priority #3)
        if solar_remaining > 0:
            exported_power = grid.export_energy(solar_remaining, time_step_hours)
            solar_to_grid = exported_power
            solar_remaining -= solar_to_grid
            
            # Remaining is curtailed
            curtailed = solar_remaining

        # Step 4: Handle Deficit (Battery -> Grid)
        deficit = load_kw - solar_to_load
        
        if deficit > 0:
            # 4a. Try Battery first (Standard deficit handling)
            requested_energy = deficit * time_step_hours
            discharged_energy = battery.discharge(requested_energy)
            battery_to_load = discharged_energy / time_step_hours
            deficit -= battery_to_load
            
            # 4b. Try Grid second
            if deficit > 0:
                grid.import_energy(deficit, time_step_hours)
                grid_to_load = deficit

        unmet_load = 0.0
        
        return {
            'solar_to_load': round(solar_to_load, 6),
            'solar_to_battery': round(solar_to_battery, 6),
            'solar_to_grid': round(solar_to_grid, 6),
            'battery_to_load': round(battery_to_load, 6),
            'grid_to_load': round(grid_to_load, 6),
            'unmet_load': round(unmet_load, 6),
            'curtailed': round(curtailed, 6)
        }

# ==============================PRODUCE_PRIORITY==========================================

    def _produce_priority(self, solar_kw, load_kw, battery, grid, time_step_hours):
        """
        PRODUCE_PRIORITY: Grid export first, battery second, house last.
        """
        solar_to_load = 0.0
        solar_to_battery = 0.0
        solar_to_grid = 0.0
        battery_to_load = 0.0
        grid_to_load = 0.0
        curtailed = 0.0
        
        solar_remaining = solar_kw
        
        # Step 1: Export Solar to Grid (Priority #1)
        if solar_remaining > 0:
            # Try to export everything
            exported_power = grid.export_energy(solar_remaining, time_step_hours)
            solar_to_grid = exported_power
            solar_remaining -= solar_to_grid # Only subtract what was successfully exported
        
        # Step 2: Charge Battery (Priority #2 - with rejected solar)
        # FIX: Check if battery is full BEFORE trying to charge
        if solar_remaining > 0 and not battery.is_full():
            offered_energy = solar_remaining * time_step_hours
            charged_energy = battery.charge(offered_energy)
            
            solar_to_battery = charged_energy / time_step_hours
            solar_remaining -= solar_to_battery
        
        # Step 3: Power House (Priority #3)
        if solar_remaining > 0:
            solar_to_load = min(solar_remaining, load_kw)
            solar_remaining -= solar_to_load
        
        # Calculate Curtailed (If Grid Full AND Battery Full AND Load Covered)
        curtailed = solar_remaining
        
        # Step 4: Handle Deficit (Battery -> Grid)
        deficit = load_kw - solar_to_load
        
        if deficit > 0:
            # 4a. Try Battery first
            requested_energy = deficit * time_step_hours
            discharged_energy = battery.discharge(requested_energy)
            battery_to_load = discharged_energy / time_step_hours
            deficit -= battery_to_load
            
            # 4b. Import from grid
            if deficit > 0:
                grid.import_energy(deficit, time_step_hours)
                grid_to_load = deficit

        unmet_load = 0.0
        
        return {
            'solar_to_load': round(solar_to_load, 6),
            'solar_to_battery': round(solar_to_battery, 6),
            'solar_to_grid': round(solar_to_grid, 6),
            'battery_to_load': round(battery_to_load, 6),
            'grid_to_load': round(grid_to_load, 6),
            'unmet_load': round(unmet_load, 6),
            'curtailed': round(curtailed, 6)
        }