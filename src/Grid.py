class Grid:
    """
    Manages energy import/export transactions with the utility grid.
    """
    
    def __init__(self, import_cost_per_kwh, export_revenue_per_kwh, 
                 export_limit_kw):
        """
        Initialize grid connection.
        
        Args:
            import_cost_per_kwh (float): Cost to import energy ($/kWh)
            export_revenue_per_kwh (float): Revenue from exporting ($/kWh)
            export_limit_kw (float): Maximum export power (kW)
        """

        self._import_cost_per_kwh = import_cost_per_kwh
        self._export_revenue_per_kwh = export_revenue_per_kwh
        self._export_limit_kw = export_limit_kw
        
        self._total_energy_imported_kwh = 0.0
        self._total_energy_exported_kwh = 0.0
        self._total_import_cost = 0.0
        self._total_export_revenue = 0.0
    
    def import_energy(self, energy_kwh):
        """
        Import (buy) energy from grid.
        
        Args:
            energy_kwh (float): Energy to import in kWh
            
        Returns:
            float: Cost of this import in dollars
        """

        # 1. Sum energy_kwh to total_imported
        self._total_energy_imported_kwh += energy_kwh
        # 2. Calculate cost
        cost = energy_kwh * self._import_cost_per_kwh
        # 3. Sum cost to total_cost
        self._total_import_cost += cost
        # 4. Return cost
        return cost
    
    def export_energy(self, energy_kwh):
        """
        Export (sell) energy to grid.
        
        Args:
            energy_kwh (float): Energy to export in kWh
            
        Returns:
            float: Actual energy exported (may be limited)
        """
    
        # 1. Apply export limit: only export up to export_limit_kw, even if more is offered
        energy_to_export = min(energy_kwh, self._export_limit_kw)
        # 2. Sum energy_to_export to total_exported
        self._total_energy_exported_kwh += energy_to_export
        # 3. Calculate revenue
        revenue = energy_to_export * self._export_revenue_per_kwh
        # 4. Sum revenue to total_revenue
        self._total_export_revenue += revenue
        # 5. Return actual energy exported
        return energy_to_export
    
    def get_total_imported(self):
        """Get total energy imported in kWh."""
        return self._total_energy_imported_kwh
        
    
    def get_total_exported(self):
        """Get total energy exported in kWh."""
        return self._total_energy_exported_kwh
    
    def get_total_cost(self):
        """Get total cost of imported energy in dollars."""

        return self._total_import_cost
    
    def get_total_revenue(self):
        """Get total revenue from exported energy in dollars."""

        return self._total_export_revenue
    
    def get_net_balance(self):
        """
        Get net financial balance.
        
        Returns:
            float: Net balance (revenue - cost) in dollars
                  Positive = profit, Negative = loss
        """

        return self._total_export_revenue - self._total_import_cost
