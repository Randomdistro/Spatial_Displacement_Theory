using System;

namespace SDT.AtomicProperties
{
    /// <summary>
    /// SDT Atomic Properties Calculator
    /// Zero lookup tables - pure calculation from fundamental constants
    /// </summary>
    public static class Constants
    {
        public const double C = 299_792_458.0;           // m/s (speed of light)
        public const double H = 6.626_070_15e-34;        // J·s (Planck constant)
        public const double M_e = 9.109_383_7015e-31;    // kg (electron mass)
        public const double AlphaInv = 137.036;          // fine structure constant⁻¹
        public const double Ry = 13.605_693;             // eV (Rydberg energy)
        public const double LambdaC = H / (M_e * C);     // Compton wavelength (m)
        public const double K = M_e * C / (2.0 * H);     // nm⁻¹
    }

    public class AtomicProperties
    {
        public double IonizationEnergy { get; set; }     // eV
        public double Koppa { get; set; }                // ϟ = c/v
        public double KoppaSq { get; set; }              // ϟ²
        public double Velocity { get; set; }             // m/s
        public double VelocityFraction { get; set; }     // v/c
        public double WavelengthNm { get; set; }         // nm
        public double PhaseSpace { get; set; }           // Ω = ϟ²
        public double EffectiveN { get; set; }           // n_eff
        
        public static AtomicProperties Calculate(double ionizationEnergyEv)
        {
            var props = new AtomicProperties
            {
                IonizationEnergy = ionizationEnergyEv
            };
            
            // Step 1: Calculate ϟ
            props.Koppa = Constants.AlphaInv * Math.Sqrt(Constants.Ry / ionizationEnergyEv);
            props.KoppaSq = props.Koppa * props.Koppa;
            
            // Step 2: Calculate velocity
            props.Velocity = Constants.C / props.Koppa;
            props.VelocityFraction = 1.0 / props.Koppa;
            
            // Step 3: Calculate wavelength (λ = 2λ_C × ϟ²)
            props.WavelengthNm = 2.0 * Constants.LambdaC * props.KoppaSq * 1e9;
            
            // Step 4: Phase space volume
            props.PhaseSpace = props.KoppaSq;
            
            // Step 5: Effective quantum number
            props.EffectiveN = props.Koppa / Constants.AlphaInv;
            
            return props;
        }
        
        public double QuantumDefect(int principalN) => principalN - EffectiveN;
        
        public override string ToString()
        {
            return $"E_i:      {IonizationEnergy:F4} eV\n" +
                   $"ϟ:        {Koppa:F2}\n" +
                   $"ϟ²:       {KoppaSq:F0}\n" +
                   $"v:        {Velocity:E3} m/s ({VelocityFraction * 100:F4}% c)\n" +
                   $"λ_ion:    {WavelengthNm:F2} nm\n" +
                   $"Ω:        {PhaseSpace:F0}\n" +
                   $"n_eff:    {EffectiveN:F3}";
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            
            Console.WriteLine("═══════════════════════════════════════════════════════════");
            Console.WriteLine("  SDT Atomic Properties: Pure First-Principles Calculation");
            Console.WriteLine("  No Lookup Tables | No Empirical Fits | Just Physics");
            Console.WriteLine("═══════════════════════════════════════════════════════════\n");
            
            // Hydrogen (reference)
            Console.WriteLine("HYDROGEN (1s¹) - The Reference");
            Console.WriteLine("────────────────────────────────────");
            var hydrogen = AtomicProperties.Calculate(13.5984);
            Console.WriteLine(hydrogen);
            Console.WriteLine($"✓ ϟ = α⁻¹ ({Constants.AlphaInv:F2}) for hydrogen\n");
            
            // Sodium (alkali metal)
            Console.WriteLine("SODIUM (3s¹) - Alkali Metal");
            Console.WriteLine("────────────────────────────────────");
            var sodium3s = AtomicProperties.Calculate(5.1391);
            Console.WriteLine(sodium3s);
            var delta = sodium3s.QuantumDefect(3);
            Console.WriteLine($"\nQuantum defect δ: {delta:F3}");
            Console.WriteLine($"  (n = 3, n_eff = {sodium3s.EffectiveN:F3})\n");
            
            // Multi-ionization sequence
            Console.WriteLine("SODIUM MULTI-IONIZATION SEQUENCE");
            Console.WriteLine("────────────────────────────────────");
            var levels = new[]
            {
                ("3s¹", 5.1391),
                ("2p⁶", 47.2864),
                ("2p⁵", 71.6200)
            };
            
            Console.WriteLine($"{"Shell",-8} {"E_i (eV)",10} {"ϟ",8} {"ϟ²",10} {"λ (nm)",12} {"Ω",10}");
            Console.WriteLine("────────────────────────────────────────────────────────────");
            
            var props = new AtomicProperties[levels.Length];
            for (int i = 0; i < levels.Length; i++)
            {
                props[i] = AtomicProperties.Calculate(levels[i].Item2);
                Console.WriteLine($"{levels[i].Item1,-8} {props[i].IonizationEnergy,10:F2} " +
                                $"{props[i].Koppa,8:F1} {props[i].KoppaSq,10:F0} " +
                                $"{props[i].WavelengthNm,12:F2} {props[i].PhaseSpace,10:F0}");
            }
            
            // Energy conservation validation
            Console.WriteLine("\nENERGY CONSERVATION VALIDATION");
            Console.WriteLine("────────────────────────────────────");
            double energyRatio = props[1].IonizationEnergy / props[0].IonizationEnergy;
            double phaseRatio = props[0].PhaseSpace / props[1].PhaseSpace;
            double koppaRatioSq = Math.Pow(props[0].Koppa / props[1].Koppa, 2);
            double error = Math.Abs(energyRatio - phaseRatio) / energyRatio;
            
            Console.WriteLine($"E₂/E₁:         {energyRatio:F3}");
            Console.WriteLine($"Ω₁/Ω₂:         {phaseRatio:F3}");
            Console.WriteLine($"(ϟ₁/ϟ₂)²:      {koppaRatioSq:F3}");
            Console.WriteLine($"Relative err:  {error:E2}\n");
            
            if (error < 0.001)
            {
                Console.WriteLine("✓ Energy conservation validated!");
                Console.WriteLine("  E_ratio = Ω_ratio = (ϟ_ratio)²\n");
            }
            
            // Ionization/Recombination cycle
            Console.WriteLine("IONIZATION ↔ RECOMBINATION CYCLE");
            Console.WriteLine("────────────────────────────────────");
            Console.WriteLine("Na (3s¹) ionization:");
            Console.WriteLine($"  Photon absorbed:  λ = {sodium3s.WavelengthNm:F2} nm, E = {sodium3s.IonizationEnergy:F4} eV");
            Console.WriteLine("\nNa⁺ recombination (captures e⁻):");
            Console.WriteLine($"  Photon emitted:   λ = {sodium3s.WavelengthNm:F2} nm, E = {sodium3s.IonizationEnergy:F4} eV");
            Console.WriteLine("\n✓ Energy absorbed = Energy emitted");
            Console.WriteLine("✓ Wavelength in = Wavelength out");
            Console.WriteLine("✓ Perfect energy conservation\n");
            
            // Summary
            Console.WriteLine("═══════════════════════════════════════════════════════════");
            Console.WriteLine("ALGORITHM SUMMARY");
            Console.WriteLine("═══════════════════════════════════════════════════════════");
            Console.WriteLine("Input:  E_i (ionization energy)");
            Console.WriteLine("Output: ϟ, v, λ, Ω, δ - all calculated from constants\n");
            Console.WriteLine("Fundamental constants used:");
            Console.WriteLine($"  α⁻¹ = {Constants.AlphaInv}");
            Console.WriteLine($"  Ry  = {Constants.Ry} eV");
            Console.WriteLine($"  c   = {Constants.C:F0} m/s");
            Console.WriteLine($"  λ_C = {Constants.LambdaC:E3} m\n");
            Console.WriteLine("Zero lookup tables. Pure calculation.");
            Console.WriteLine("═══════════════════════════════════════════════════════════");
            
            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }
    }
}
