#!/usr/bin/env python3
"""
Configuration for ML models in Git Hook DJ.
"""

import json
import os
from pathlib import Path

class MLConfig:
    """Configuration manager for ML models."""
    
    def __init__(self, config_file: str = ".git/ml_config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from file or create default."""
        default_config = {
            "use_transformer": True,
            "model_preference": "auto",  # auto, transformer, sklearn
            "download_models": True,
            "cache_models": True,
            "fallback_to_sklearn": True
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
                return default_config
        else:
            return default_config
    
    def save_config(self):
        """Save configuration to file."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")
    
    def get(self, key: str, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set a configuration value."""
        self.config[key] = value
        self.save_config()
    
    def use_transformer(self) -> bool:
        """Check if transformer models should be used."""
        return self.get("use_transformer", True)
    
    def set_transformer(self, use: bool):
        """Set whether to use transformer models."""
        self.set("use_transformer", use)
    
    def get_model_preference(self) -> str:
        """Get model preference: auto, transformer, or sklearn."""
        return self.get("model_preference", "auto")
    
    def set_model_preference(self, preference: str):
        """Set model preference."""
        if preference in ["auto", "transformer", "sklearn"]:
            self.set("model_preference", preference)
        else:
            raise ValueError("Model preference must be 'auto', 'transformer', or 'sklearn'")
    
    def should_download_models(self) -> bool:
        """Check if models should be downloaded."""
        return self.get("download_models", True)
    
    def set_download_models(self, download: bool):
        """Set whether to download models."""
        self.set("download_models", download)
    
    def should_fallback_to_sklearn(self) -> bool:
        """Check if should fallback to sklearn if transformer fails."""
        return self.get("fallback_to_sklearn", True)
    
    def set_fallback_to_sklearn(self, fallback: bool):
        """Set whether to fallback to sklearn."""
        self.set("fallback_to_sklearn", fallback)
    
    def get_effective_model_choice(self) -> bool:
        """Get the effective model choice based on preferences."""
        preference = self.get_model_preference()
        
        if preference == "transformer":
            return True
        elif preference == "sklearn":
            return False
        else:  # auto
            return self.use_transformer()
    
    def show_config(self):
        """Display current configuration."""
        print("🤖 ML Configuration:")
        print(f"   Model Preference: {self.get_model_preference()}")
        print(f"   Use Transformer: {self.use_transformer()}")
        print(f"   Download Models: {self.should_download_models()}")
        print(f"   Fallback to Sklearn: {self.should_fallback_to_sklearn()}")
        print(f"   Effective Choice: {'transformer' if self.get_effective_model_choice() else 'sklearn'}")


def main():
    """CLI for ML configuration."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Configure ML models for Git Hook DJ")
    parser.add_argument("--show", action="store_true", help="Show current configuration")
    parser.add_argument("--use-transformer", action="store_true", help="Use transformer models")
    parser.add_argument("--use-sklearn", action="store_true", help="Use sklearn models")
    parser.add_argument("--preference", choices=["auto", "transformer", "sklearn"], 
                       help="Set model preference")
    parser.add_argument("--no-download", action="store_true", help="Disable model downloads")
    parser.add_argument("--no-fallback", action="store_true", help="Disable sklearn fallback")
    
    args = parser.parse_args()
    
    config = MLConfig()
    
    if args.show:
        config.show_config()
    
    if args.use_transformer:
        config.set_transformer(True)
        print("✅ Set to use transformer models")
    
    if args.use_sklearn:
        config.set_transformer(False)
        print("✅ Set to use sklearn models")
    
    if args.preference:
        config.set_model_preference(args.preference)
        print(f"✅ Set model preference to {args.preference}")
    
    if args.no_download:
        config.set_download_models(False)
        print("✅ Disabled model downloads")
    
    if args.no_fallback:
        config.set_fallback_to_sklearn(False)
        print("✅ Disabled sklearn fallback")
    
    if not any([args.show, args.use_transformer, args.use_sklearn, 
                args.preference, args.no_download, args.no_fallback]):
        config.show_config()


if __name__ == "__main__":
    main()
