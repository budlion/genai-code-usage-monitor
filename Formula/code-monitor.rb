# Homebrew Formula for GenAI Code Usage Monitor
# Installation: brew install --formula ./Formula/code-monitor.rb

class CodeMonitor < Formula
  desc "GenAI Code Usage Monitor - Real-time AI API usage monitor for Generative AI platforms (OpenAI, Claude)"
  homepage "https://github.com/yourusername/genai-code-usage-monitor"
  url "file://#{Dir.pwd}"
  version "2.0.0"
  license "MIT"

  depends_on "python@3.11"

  def install
    # Create a virtualenv in libexec
    venv = virtualenv_create(libexec, "python3")

    # Install dependencies
    system libexec/"bin/pip", "install", "--upgrade", "pip"
    system libexec/"bin/pip", "install", "-r", "requirements.txt"

    # Install the package
    system libexec/"bin/pip", "install", "-e", "."

    # Create wrapper script
    (bin/"code-monitor").write_env_script libexec/"bin/python3",
      "-m", "genai_code_usage_monitor",
      :PYTHONPATH => "#{prefix}/src"

    # Install man page if exists
    # man1.install "docs/code-monitor.1" if File.exist?("docs/code-monitor.1")
  end

  def post_install
    ohai "GenAI Code Usage Monitor installed successfully!"
    ohai ""
    ohai "Quick start:"
    ohai "  code-monitor                    # Monitor both platforms"
    ohai "  code-monitor --platform codex   # Monitor OpenAI Codex only"
    ohai "  code-monitor --platform claude  # Monitor Claude Code only"
    ohai "  code-monitor --help             # Show all options"
    ohai ""
    ohai "Configuration:"
    ohai "  Codex data:  ~/.codex-monitor/"
    ohai "  Claude data: ~/.claude-monitor/"
  end

  test do
    system "#{bin}/code-monitor", "--help"
  end
end
