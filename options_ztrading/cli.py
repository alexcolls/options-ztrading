"""Command-line interface for options-ztrading."""
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .config import (
    DEFAULT_CONTRACT,
    DEFAULT_EXPIRATION,
    DEFAULT_LIMIT,
    MAX_WORKERS,
    DATA_DIR,
    POLYGON_API_KEY,
)
from .services.tickers import (
    fetch_all_tickers,
    save_tickers_to_csv,
    load_tickers_from_csv,
)
from .services.options import (
    fetch_options_snapshot,
    save_options_to_csv,
    ContractType,
)

app = typer.Typer(
    name="options",
    help="📈 Terminal-based options data fetcher from Polygon.io",
    add_completion=False,
)
console = Console()


@app.command()
def fetch_tickers(
    out: Optional[Path] = typer.Option(
        None,
        "--out",
        "-o",
        help="Output CSV file path",
    ),
    limit: int = typer.Option(
        1000,
        "--limit",
        "-l",
        help="Maximum tickers per API request",
    ),
    active_only: bool = typer.Option(
        True,
        "--active-only",
        help="Fetch only active tickers",
    ),
):
    """🎯 Fetch all stock tickers from Polygon.io."""
    try:
        console.print("[bold yellow]Fetching tickers from Polygon.io...[/]")

        tickers = fetch_all_tickers(limit=limit, active=active_only)

        if not tickers:
            console.print("[bold red]No tickers found![/]")
            raise typer.Exit(1)

        # Save to CSV
        output_path = save_tickers_to_csv(tickers, out)

        # Display summary
        table = Table(title="Ticker Fetch Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Total Tickers", str(len(tickers)))
        table.add_row("Output File", str(output_path))
        table.add_row("Sample Tickers", ", ".join(tickers[:5]) + "...")

        console.print(table)
        console.print(f"[bold green]✅ Successfully saved {len(tickers)} tickers![/]")

    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/]")
        raise typer.Exit(1)


@app.command()
def fetch_options(
    expiration: str = typer.Option(
        DEFAULT_EXPIRATION,
        "--expiration",
        "-e",
        help="Options expiration date (YYYY-MM-DD)",
    ),
    contract: ContractType = typer.Option(
        DEFAULT_CONTRACT,
        "--contract",
        "-c",
        help="Contract type: call, put, or both",
    ),
    limit: int = typer.Option(
        DEFAULT_LIMIT,
        "--limit",
        "-l",
        help="Maximum contracts per ticker",
    ),
    tickers: Optional[Path] = typer.Option(
        None,
        "--tickers",
        "-t",
        help="Path to tickers CSV file",
    ),
    out: Optional[Path] = typer.Option(
        None,
        "--out",
        "-o",
        help="Output CSV file path",
    ),
    max_workers: int = typer.Option(
        MAX_WORKERS,
        "--max-workers",
        "-w",
        help="Maximum concurrent workers",
    ),
):
    """💰 Fetch options snapshots for multiple tickers."""
    try:
        # Load tickers
        if tickers:
            ticker_list = load_tickers_from_csv(tickers)
        else:
            default_path = DATA_DIR / "tickers.csv"
            if not default_path.exists():
                console.print(
                    "[bold red]No tickers file found! "
                    "Run 'options fetch-tickers' first.[/]"
                )
                raise typer.Exit(1)
            ticker_list = load_tickers_from_csv()

        console.print(
            f"[bold yellow]Fetching {contract} options for "
            f"{len(ticker_list)} tickers (exp: {expiration})...[/]"
        )

        # Fetch options
        df = fetch_options_snapshot(
            tickers=ticker_list,
            expiration=expiration,
            contract_type=contract,
            limit=limit,
            max_workers=max_workers,
            show_progress=True,
        )

        if df.empty:
            console.print("[bold red]No options data retrieved![/]")
            raise typer.Exit(1)

        # Save to CSV
        output_path = save_options_to_csv(
            df,
            output_path=out,
            contract_type=contract,
            expiration=expiration,
        )

        # Display summary
        table = Table(title="Options Fetch Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Total Records", str(len(df)))
        table.add_row("Unique Tickers", str(df["ticker"].nunique()))
        table.add_row("Contract Type", contract)
        table.add_row("Expiration", expiration)
        table.add_row("Output File", str(output_path))

        console.print(table)
        console.print(f"[bold green]✅ Successfully saved {len(df)} options records![/]")

    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/]")
        raise typer.Exit(1)


@app.command()
def verify():
    """✔️ Verify environment setup and configuration."""
    console.print(Panel.fit("🔍 Verifying Environment Setup", style="bold cyan"))

    checks = []
    all_good = True

    # Check API key
    if POLYGON_API_KEY:
        checks.append(("Polygon API Key", "✅ Configured", "green"))
    else:
        checks.append(("Polygon API Key", "❌ Missing", "red"))
        all_good = False

    # Check data directory
    if DATA_DIR.exists() and DATA_DIR.is_dir():
        checks.append(("Data Directory", f"✅ {DATA_DIR}", "green"))
    else:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            checks.append(("Data Directory", f"✅ Created: {DATA_DIR}", "yellow"))
        except Exception as e:
            checks.append(("Data Directory", f"❌ Error: {e}", "red"))
            all_good = False

    # Check tickers file
    tickers_file = DATA_DIR / "tickers.csv"
    if tickers_file.exists():
        try:
            tickers = load_tickers_from_csv()
            checks.append(("Tickers File", f"✅ {len(tickers)} tickers", "green"))
        except Exception:
            checks.append(("Tickers File", "⚠️ Exists but unreadable", "yellow"))
    else:
        checks.append(("Tickers File", "ℹ️ Not found (run fetch-tickers)", "blue"))

    # Display results
    table = Table(title="Configuration Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status")

    for component, status, color in checks:
        table.add_row(component, f"[{color}]{status}[/]")

    console.print(table)

    if all_good:
        console.print("[bold green]✅ Environment is properly configured![/]")
    else:
        console.print(
            "[bold yellow]⚠️ Some configuration items need attention. "
            "Check your .env file.[/]"
        )
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
}