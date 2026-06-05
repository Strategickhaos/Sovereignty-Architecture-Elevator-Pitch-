#!/usr/bin/env python3
"""
Simple test suite for Loihi Neuromorphic Integration
Validates core functionality of all modules
"""

import sys
import traceback

def test_eeg_processor():
    """Test EEG processing module"""
    print("Testing EEG Processor...", end=" ")
    try:
        from loihi_eeg_processor import LoihiEEGProcessor, EEGConfig, SpikeEncoding
        
        # Create processor
        config = EEGConfig(sample_rate=256, num_channels=8)
        processor = LoihiEEGProcessor()
        
        # Generate and process simulated data
        import numpy as np
        eeg_data = np.random.randn(256, 8)  # 1 second of data
        results = processor.process(raw_data=eeg_data)
        
        # Validate outputs
        assert 'spike_trains' in results
        assert results['spike_trains'].shape[-1] == 8
        
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        traceback.print_exc()
        return False


def test_loihi_simulator():
    """Test Loihi SNN simulator"""
    print("Testing Loihi SNN Simulator...", end=" ")
    try:
        from loihi_snn_simulator import LoihiSNNSimulator, LIFNeuronConfig
        import numpy as np
        
        # Create simulator
        simulator = LoihiSNNSimulator(
            layer_sizes=[8, 16, 8],
            dt=0.001
        )
        
        # Run simulation
        spike_trains = np.random.random((100, 8)) < 0.1
        results = simulator.run(spike_trains, verbose=False)
        
        # Validate outputs
        assert 'total_output_spikes' in results
        assert 'avg_power_mw' in results
        
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        traceback.print_exc()
        return False


def test_genomics_reconstructor():
    """Test genomics reconstruction module"""
    print("Testing Genomics Reconstructor...", end=" ")
    try:
        from genomics_recon import GenomicsReconstructor, DNAEncoder
        
        # Create reconstructor
        reconstructor = GenomicsReconstructor()
        
        # Test DNA encoding
        sequence = "ACGTACGT"
        spikes = DNAEncoder.sequence_to_spikes(sequence)
        assert spikes.shape == (8, 4)
        
        # Test gene info lookup
        gene_info = reconstructor.database.get_gene_info("SCN1A")
        assert gene_info is not None
        assert gene_info.disease == "Dravet Syndrome"
        
        # Test EEG correlation
        eeg_markers = ["spike_wave", "polyspike"]
        correlation = reconstructor.correlate_eeg_phenotype(eeg_markers)
        assert 'candidate_genes' in correlation
        
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        traceback.print_exc()
        return False


def test_trig6_evaluator():
    """Test TRIG6 evaluation"""
    print("Testing TRIG6 Evaluator...", end=" ")
    try:
        from trig6_runner import TRIG6Evaluator
        import numpy as np
        
        evaluator = TRIG6Evaluator()
        
        # Create test data
        eeg_data = np.random.randn(10, 256, 8)
        embeddings = np.random.randn(100, 16)
        
        # Evaluate
        metrics = evaluator.evaluate(eeg_data, embeddings)
        
        # Validate outputs
        assert 'theta' in metrics
        assert 'R' in metrics
        assert 'I' in metrics
        assert 'G' in metrics
        assert 'sixth_sense' in metrics
        assert 'state' in metrics
        
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        traceback.print_exc()
        return False


def test_pipeline_config():
    """Test pipeline configuration"""
    print("Testing Pipeline Config...", end=" ")
    try:
        import yaml
        
        with open('neuralink_infusion_pipeline.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate structure
        assert 'metadata' in config
        assert 'pipeline' in config
        assert 'stages' in config['pipeline']
        assert len(config['pipeline']['stages']) == 7
        
        # Check stage names
        stage_names = [s['name'] for s in config['pipeline']['stages']]
        expected = ['eeg_ingest', 'spike_encoding', 'loihi_deploy', 
                   'trig6_eval', 'codon_evolution', 'genomics_recon', 
                   'integration_deploy']
        assert stage_names == expected
        
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 80)
    print("LOIHI NEUROMORPHIC INTEGRATION - TEST SUITE")
    print("=" * 80)
    print()
    
    tests = [
        test_pipeline_config,
        test_eeg_processor,
        test_loihi_simulator,
        test_genomics_reconstructor,
        test_trig6_evaluator,
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print()
    print("=" * 80)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("=" * 80)
    
    if all(results):
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed. See above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
